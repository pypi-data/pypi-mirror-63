#!/usr/bin/python3

"""
This file is part of pycos project. See https://pycos.sourceforge.io for details.

This module provides API for creating distributed communicating
processes. 'Computation' class should be used to package computation components
(Python generator functions, Python functions, files, classes, modules) and then
schedule runs that create remote tasks at remote server processes running
'dispycosnode.py'.

See 'dispycos_client*.py' files in 'examples' directory for various use cases.
"""

import os
import sys
import inspect
import hashlib
import collections
import time
import shutil
import operator
import functools
import re
import copy
import stat

import pycos
import pycos.netpycos
import pycos.config
from pycos import Task, SysTask, logger

__author__ = "Giridhar Pemmasani (pgiri@yahoo.com)"
__copyright__ = "Copyright (c) 2014-2015 Giridhar Pemmasani"
__license__ = "Apache 2.0"
__url__ = "https://pycos.sourceforge.io"

__all__ = ['Scheduler', 'Computation', 'DispycosStatus', 'DispycosTaskInfo',
           'DispycosNodeInfo', 'DispycosNodeAvailInfo', 'DispycosNodeAllocate']

# status about nodes / servers are sent with this structure
DispycosStatus = collections.namedtuple('DispycosStatus', ['status', 'info'])
DispycosTaskInfo = collections.namedtuple('DispycosTaskInfo', ['task', 'args', 'kwargs',
                                                               'start_time'])
DispycosNodeInfo = collections.namedtuple('DispycosNodeInfo', ['name', 'addr', 'cpus', 'platform',
                                                               'avail_info'])
MsgTimeout = pycos.config.MsgTimeout
MinPulseInterval = pycos.config.MinPulseInterval
MaxPulseInterval = pycos.config.MaxPulseInterval
logger.name = 'dispycos'
# PyPI / pip packaging adjusts assertion below for Python 3.7+
assert sys.version_info.major == 3 and sys.version_info.minor < 7, \
    ('"%s" is not suitable for Python version %s.%s; use file installed by pip instead' %
     (__file__, sys.version_info.major, sys.version_info.minor))


class DispycosNodeAvailInfo(object):
    """Node availability status is indicated with this class.  'cpu' is
    available CPU in percent in the range 0 to 100. 0 indicates node is busy
    executing tasks on all CPUs and 100 indicates node is not busy at all.
    """

    def __init__(self, location, cpu, memory, disk, swap):
        self.location = location
        self.cpu = cpu
        self.memory = memory
        self.disk = disk
        self.swap = swap


class DispycosNodeAllocate(object):
    """Allocation of nodes can be customized by specifying 'nodes' of Computation
    with DispycosNodeAllocate instances.

    'node' must be hostname or IP address (with possibly '*' to match rest of IP
    address), 'port must be TCP port used by node (only if 'node' doesn't have
    '*'), 'cpus', if given, must be number of servers running on that node if
    positive, or number of CPUs not to use if negative, 'memory' is minimum
    available memory in bytes, 'disk' is minimum available disk space (on the
    partition where dispycosnode servers are running from), and 'platform' is
    regular expression to match output of"platform.platform()" on that node,
    e.g., "Linux.*x86_64" to accept only nodes that run 64-bit Linux.
    """

    def __init__(self, node, port=None, platform='', cpus=None, memory=None, disk=None):
        if node.find('*') < 0:
            self.ip_rex = pycos.Pycos.host_ipaddr(node)
        else:
            self.ip_rex = node

        if self.ip_rex:
            self.ip_rex = self.ip_rex.replace('.', '\\.').replace('*', '.*')
        else:
            logger.warning('node "%s" is invalid', node)
            self.ip_rex = ''

        self.port = port
        self.platform = platform.lower()
        self.cpus = cpus
        self.memory = memory
        self.disk = disk

    def allocate(self, ip_addr, name, platform, cpus, memory, disk):
        """When a node is found, scheduler calls this method with IP address, name,
        CPUs, memory and disk available on that node. This method should return
        a number indicating number of CPUs to use. If return value is 0, the
        node is not used; if the return value is < 0, this allocation is ignored
        (next allocation in the 'nodes' list, if any, is applied).
        """
        if (self.platform and not re.search(self.platform, platform)):
            return -1
        if ((self.memory and memory and self.memory > memory) or
            (self.disk and disk and self.disk > disk)):
            return 0
        if not isinstance(self.cpus, int):
            return cpus
        if self.cpus == 0:
            return 0
        elif self.cpus > 0:
            if self.cpus > cpus:
                return 0
            return self.cpus
        else:
            cpus += self.cpus
            if cpus < 0:
                return 0
            return cpus

    def __getstate__(self):
        state = {}
        for attr in ['ip_rex', 'port', 'platform', 'cpus', 'memory', 'disk']:
            state[attr] = getattr(self, attr)
        return state


class Computation(object):
    """Packages components to distribute to remote pycos schedulers to create
    (remote) tasks.
    """

    def __init__(self, components, nodes=[], status_task=None, node_setup=None, server_setup=None,
                 disable_nodes=False, disable_servers=False, peers_communicate=False,
                 pulse_interval=(5*MinPulseInterval), node_allocations=[],
                 ping_interval=None, zombie_period=None, abandon_zombie_nodes=False):
        """'components' should be a list, each element of which is either a
        module, a (generator or normal) function, path name of a file, a class
        or an object (in which case the code for its class is sent).

        'pulse_interval' is interval (number of seconds) used for heart beat
        messages to check if client / scheduler / server is alive. If the other
        side doesn't reply to 5 heart beat messages, it is treated as dead.
        """

        if pulse_interval < MinPulseInterval or pulse_interval > MaxPulseInterval:
            raise Exception('"pulse_interval" must be at least %s and at most %s' %
                            (MinPulseInterval, MaxPulseInterval))
        if ping_interval and ping_interval < pulse_interval:
            raise Exception('"ping_interval" must be at least %s' % (pulse_interval))
        if not isinstance(nodes, list):
            raise Exception('"nodes" must be list of strings or DispycosNodeAllocate instances')
        if node_allocations:
            logger.warning('  WARNING: "node_allocations" is deprecated; use "nodes" instead')
            if not isinstance(node_allocations, list):
                raise Exception('"node_allocations" must be list of DispycosNodeAllocate instances')
            nodes.extend(node_allocations)
        if any(not isinstance(_, (DispycosNodeAllocate, str)) for _ in nodes):
            raise Exception('"nodes" must be list of strings or DispycosNodeAllocate instances')
        if status_task and not isinstance(status_task, Task):
            raise Exception('status_task must be Task instance')
        if node_setup and not inspect.isgeneratorfunction(node_setup):
            raise Exception('"node_setup" must be a task (generator function)')
        if server_setup and not inspect.isgeneratorfunction(server_setup):
            raise Exception('"server_setup" must be a task (generator function)')
        if (disable_nodes or disable_servers) and not status_task:
            raise Exception('status_task must be given when nodes or servers are disabled')
        if zombie_period:
            if zombie_period < 5*pulse_interval:
                raise Exception('"zombie_period" must be at least 5*pulse_interval')
        elif zombie_period is None:
            zombie_period = 10*pulse_interval

        if not isinstance(components, list):
            components = [components]

        self._code = ''
        self._xfer_funcs = set()
        self._xfer_files = []
        self._auth = None
        self.scheduler = None
        self._pulse_task = None
        if zombie_period:
            self._pulse_interval = min(pulse_interval, zombie_period / 3)
        else:
            self._pulse_interval = pulse_interval
        self._ping_interval = ping_interval
        self._zombie_period = zombie_period
        if nodes:
            self._node_allocations = [node if isinstance(node, DispycosNodeAllocate)
                                      else DispycosNodeAllocate(node) for node in nodes]
            self._node_allocations.append(DispycosNodeAllocate('*', cpus=0))
        else:
            self._node_allocations = [DispycosNodeAllocate('*')]
        self.status_task = status_task
        if node_setup:
            components.append(node_setup)
            self._node_setup = node_setup.__name__
        else:
            self._node_setup = None
        if server_setup:
            components.append(server_setup)
            self._server_setup = server_setup.__name__
        else:
            self._server_setup = None
        self._peers_communicate = bool(peers_communicate)
        self._disable_nodes = bool(disable_nodes)
        self._disable_servers = bool(disable_servers)
        self._abandon_zombie = bool(abandon_zombie_nodes)

        depends = set()
        cwd = os.getcwd()
        for dep in components:
            if isinstance(dep, str) or inspect.ismodule(dep):
                if inspect.ismodule(dep):
                    name = dep.__file__
                    if name.endswith('.pyc'):
                        name = name[:-1]
                    if not name.endswith('.py'):
                        raise Exception('Invalid module "%s" - must be python source.' % dep)
                    if name.startswith(cwd):
                        dst = os.path.dirname(name[len(cwd):].lstrip(os.sep))
                    elif dep.__package__:
                        dst = dep.__package__.replace('.', os.sep)
                    else:
                        dst = os.path.dirname(dep.__name__.replace('.', os.sep))
                else:
                    name = os.path.abspath(dep)
                    if name.startswith(cwd):
                        dst = os.path.dirname(name[len(cwd):].lstrip(os.sep))
                    else:
                        dst = '.'
                if name in depends:
                    continue
                try:
                    with open(name, 'rb') as fd:
                        pass
                except Exception:
                    raise Exception('File "%s" is not valid' % name)
                self._xfer_files.append((name, dst, os.sep))
                depends.add(name)
            elif (inspect.isgeneratorfunction(dep) or inspect.isfunction(dep) or
                  inspect.isclass(dep) or hasattr(dep, '__class__')):
                if inspect.isgeneratorfunction(dep) or inspect.isfunction(dep):
                    name = dep.__name__
                elif inspect.isclass(dep):
                    name = dep.__name__
                elif hasattr(dep, '__class__') and inspect.isclass(dep.__class__):
                    dep = dep.__class__
                    name = dep.__name__
                if name in depends:
                    continue
                depends.add(name)
                self._xfer_funcs.add(name)
                self._code += '\n' + inspect.getsource(dep).lstrip()
            else:
                raise Exception('Invalid computation: %s' % dep)
        # check code can be compiled
        compile(self._code, '<string>', 'exec')
        # Under Windows dispycos server may send objects with '__mp_main__'
        # scope, so make an alias to '__main__'.  Do so even if scheduler is not
        # running on Windows; it is possible the client is not Windows, but a
        # node is.
        if os.name == 'nt' and '__mp_main__' not in sys.modules:
            sys.modules['__mp_main__'] = sys.modules['__main__']

    def schedule(self, location=None, timeout=None):
        """Schedule computation for execution. Must be used with 'yield' as
        'result = yield compute.schedule()'. If scheduler is executing other
        computations, this will block until scheduler processes them
        (computations are processed in the order submitted).
        """

        if self._auth is not None:
            raise StopIteration(0)
        self._auth = ''
        if self.status_task is not None and not isinstance(self.status_task, Task):
            raise StopIteration(-1)

        self.scheduler = yield SysTask.locate('dispycos_scheduler', location=location,
                                              timeout=MsgTimeout)
        if not isinstance(self.scheduler, Task):
            raise StopIteration(-1)

        def _schedule(self, task=None):
            self._pulse_task = SysTask(self._pulse_proc)
            msg = {'req': 'schedule', 'computation': pycos.serialize(self), 'client': task}
            self.scheduler.send(msg)
            self._auth = yield task.receive(timeout=MsgTimeout)
            if not isinstance(self._auth, str):
                logger.debug('Could not send computation to scheduler %s: %s',
                             self.scheduler, self._auth)
                raise StopIteration(-1)
            SysTask.scheduler().atexit(10, lambda: SysTask(self.close))
            if task.location != self.scheduler.location:
                for xf, dst, sep in self._xfer_files:
                    drive, xf = os.path.splitdrive(xf)
                    if xf.startswith(sep):
                        xf = os.path.join(os.sep, *(xf.split(sep)))
                    else:
                        xf = os.path.join(*(xf.split(sep)))
                    xf = drive + xf
                    dst = os.path.join(self._auth, os.path.join(*(dst.split(sep))))
                    if (yield pycos.Pycos.instance().send_file(
                       self.scheduler.location, xf, dir=dst, timeout=MsgTimeout)) < 0:
                        logger.warning('Could not send file "%s" to scheduler', xf)
                        yield self.close()
                        raise StopIteration(-1)
            msg = {'req': 'await', 'auth': self._auth, 'client': task}
            self.scheduler.send(msg)
            resp = yield task.receive(timeout=timeout)
            if (isinstance(resp, dict) and resp.get('auth') == self._auth and
               resp.get('resp') == 'scheduled'):
                raise StopIteration(0)
            else:
                yield self.close()
                raise StopIteration(-1)

        yield Task(_schedule, self).finish()

    def nodes(self):
        """Get list of addresses of nodes initialized for this computation. Must
        be used with 'yield' as 'yield compute.nodes()'.
        """

        def _nodes(self, task=None):
            msg = {'req': 'nodes', 'auth': self._auth, 'client': task}
            if (yield self.scheduler.deliver(msg, timeout=MsgTimeout)) == 1:
                yield task.receive(MsgTimeout)
            else:
                raise StopIteration([])

        yield Task(_nodes, self).finish()

    def servers(self):
        """Get list of Location instances of servers initialized for this
        computation. Must be used with 'yield' as 'yield compute.servers()'.
        """

        def _servers(self, task=None):
            msg = {'req': 'servers', 'auth': self._auth, 'client': task}
            if (yield self.scheduler.deliver(msg, timeout=MsgTimeout)) == 1:
                yield task.receive(MsgTimeout)
            else:
                raise StopIteration([])

        yield Task(_servers, self).finish()

    def tasks(self, where):
        """Get list of tasks at given node or server for this computation.
        Must be used with 'yield' as 'yield compute.tasks()'.

        """

        def _tasks(self, task=None):
            msg = {'req': 'tasks', 'auth': self._auth, 'client': task, 'at': where}
            if (yield self.scheduler.deliver(msg, timeout=MsgTimeout)) == 1:
                yield task.receive(MsgTimeout)
            else:
                raise StopIteration([])

        yield Task(_tasks, self).finish()

    def close(self, await_async=False, timeout=None):
        """Close computation. Must be used with 'yield' as 'yield
        compute.close()'.
        """

        def _close(self, done, task=None):
            msg = {'req': 'close_computation', 'auth': self._auth, 'client': task,
                   'await_async': bool(await_async)}
            self.scheduler.send(msg)
            msg = yield task.receive(timeout=timeout)
            if msg != 'closed':
                logger.warning('%s: closing computation failed?', self._auth)
            self._auth = None
            if self._pulse_task:
                yield self._pulse_task.send('quit')
                self._pulse_task = None
            done.set()

        if self._auth:
            done = pycos.Event()
            SysTask(_close, self, done)
            yield done.wait()

    def run_at(self, where, gen, *args, **kwargs):
        """Must be used with 'yield' as

        'rtask = yield computation.run_at(where, gen, ...)'

        Run given generator function 'gen' with arguments 'args' and 'kwargs' at
        remote server 'where'.  If the request is successful, 'rtask' will be a
        (remote) task; check result with 'isinstance(rtask,
        pycos.Task)'. The generator is expected to be (mostly) CPU bound and
        until this is finished, another CPU bound task will not be
        submitted at same server.

        If 'where' is a string, it is assumed to be IP address of a node, in
        which case the task is scheduled at that node on a server at that
        node. If 'where' is a Location instance, it is assumed to be server
        location in which case the task is scheduled at that server.

        'gen' must be generator function, as it is used to run task at
        remote location.
        """
        yield self._run_request('run_async', where, 1, gen, *args, **kwargs)

    def run(self, gen, *args, **kwargs):
        """Run CPU bound task at any remote server; see 'run_at'
        above.
        """
        yield self._run_request('run_async', None, 1, gen, *args, **kwargs)

    def run_result_at(self, where, gen, *args, **kwargs):
        """Must be used with 'yield' as

        'rtask = yield computation.run_result_at(where, gen, ...)'

        Whereas 'run_at' and 'run' return remote task instance,
        'run_result_at' and 'run_result' wait until remote task is
        finished and return the result of that remote task (i.e., either
        the value of 'StopIteration' or the last value 'yield'ed).

        'where', 'gen', 'args', 'kwargs' are as explained in 'run_at'.
        """
        yield self._run_request('run_result', where, 1, gen, *args, **kwargs)

    def run_result(self, gen, *args, **kwargs):
        """Run CPU bound task at any remote server and return result of
        that task; see 'run_result_at' above.
        """
        yield self._run_request('run_result', None, 1, gen, *args, **kwargs)

    def run_async_at(self, where, gen, *args, **kwargs):
        """Must be used with 'yield' as

        'rtask = yield computation.run_async_at(where, gen, ...)'

        Run given generator function 'gen' with arguments 'args' and 'kwargs' at
        remote server 'where'.  If the request is successful, 'rtask' will be a
        (remote) task; check result with 'isinstance(rtask,
        pycos.Task)'. The generator is supposed to be (mostly) I/O bound and
        not consume CPU time. Unlike other 'run' variants, tasks created
        with 'async' are not "tracked" by scheduler (see online documentation for
        more details).

        If 'where' is a string, it is assumed to be IP address of a node, in
        which case the task is scheduled at that node on a server at that
        node. If 'where' is a Location instance, it is assumed to be server
        location in which case the task is scheduled at that server.

        'gen' must be generator function, as it is used to run task at
        remote location.
        """
        yield self._run_request('run_async', where, 0, gen, *args, **kwargs)

    def run_async(self, gen, *args, **kwargs):
        """Run I/O bound task at any server; see 'run_async_at'
        above.
        """
        yield self._run_request('run_async', None, 0, gen, *args, **kwargs)

    def run_results(self, gen, iter):
        """Must be used with 'yield', as for example,
        'results = yield scheduler.map_results(generator, list_of_tuples)'.

        Execute generator 'gen' with arguments from given iterable. The return
        value is list of results that correspond to executing 'gen' with
        arguments in iterable in the same order.
        """
        tasks = []
        append_task = tasks.append
        for params in iter:
            if not isinstance(params, tuple):
                if hasattr(params, '__iter__'):
                    params = tuple(params)
                else:
                    params = (params,)
            append_task(Task(self.run_result, gen, *params))
        results = [None] * len(tasks)
        for i, task in enumerate(tasks):
            results[i] = yield task.finish()
        raise StopIteration(results)

    def enable_node(self, ip_addr, *setup_args):
        """If computation disabled nodes (with 'disabled_nodes=True' when
        Computation is constructed), nodes are not automatically used by the
        scheduler until nodes are enabled with 'enable_node'.

        'ip_addr' must be either IP address or host name of the node to be
        enabled.

        'setup_args' is arguments passed to 'node_setup' function specific to
        that node. If 'node_setup' succeeds (i.e., finishes with value 0), the
        node is used for computations.
        """
        if self.scheduler:
            if isinstance(ip_addr, pycos.Location):
                ip_addr = ip_addr.addr
            self.scheduler.send({'req': 'enable_node', 'auth': self._auth, 'addr': ip_addr,
                                 'setup_args': setup_args})

    def enable_server(self, location, *setup_args):
        """If computation disabled servers (with 'disabled_servers=True' when
        Computation is constructed), servers are not automatically used by the
        scheduler until they are enabled with 'enable_server'.

        'location' must be Location instance of the server to be enabled.

        'setup_args' is arguments passed to 'server_setup' function specific to
        that server. If 'server_setup' succeeds (i.e., finishes with value 0), the
        server is used for computations.
        """
        if self.scheduler:
            self.scheduler.send({'req': 'enable_server', 'auth': self._auth, 'server': location,
                                 'setup_args': setup_args})

    def suspend_node(self, location):
        """Suspend submitting jobs (tasks) at this node. Any currently running
        tasks are left running.
        """
        if self.scheduler:
            self.scheduler.send({'req': 'suspend_node', 'auth': self._auth, 'addr': location})

    def resume_node(self, location):
        """Resume submitting jobs (tasks) at this node.
        """
        if self.scheduler:
            self.scheduler.send({'req': 'enable_node', 'auth': self._auth, 'addr': location})

    def suspend_server(self, location):
        """Suspend submitting jobs (tasks) at this server. Any currently running
        tasks are left running.
        """
        if self.scheduler:
            self.scheduler.send({'req': 'suspend_server', 'auth': self._auth, 'server': location})

    def resume_server(self, location):
        """Resume submitting jobs (tasks) at this server.
        """
        if self.scheduler:
            self.scheduler.send({'req': 'enable_server', 'auth': self._auth, 'server': location})

    def abandon_zombie(self, location, flag):
        """If a node at given location is deemed zombie (i.e., no response in 'zombie_period'),
        then abandon any jobs running on servers on that node. If a node is detected later,
        it will be treated as new (instance of) node.

        'location' can be either Location instance of any server at the node or of the node
        itself, IP address of node or None. If 'location' is None, then all nodes currently used
        by computation and any nodes added for computation will be abandoned (when they become
        zombies) as well.

        'flag' must be either True or False indicating whether nodes would be abandoned or not.

        """
        if self.scheduler:
            if isinstance(location, pycos.Location):
                location = location.addr
            self.scheduler.send({'req': 'abandon_zombie', 'auth': self._auth, 'addr': location,
                                 'flag': bool(flag)})

    def close_node(self, location, terminate=False):
        """Close node at given location, which can be either a Location instance (of any server
        at that node or of node itself) or IP address. After this call, no more tasks are
        scheduled at that node.

        If 'terminate' is True, any tasks running at any of the servers at the node are terminated
        without waiting for them to finish. If it is False, the node will wait until tasks finish
        before closing.
        """
        if self.scheduler:
            if isinstance(location, pycos.Location):
                location = location.addr
            self.scheduler.send({'req': 'close_node', 'auth': self._auth, 'addr': location,
                                 'terminate': bool(terminate)})

    def node_allocate(self, node_allocate):
        """Request scheduler to add 'node_allocate' to any previously sent
        'node_allocations'.
        """
        if not isinstance(node_allocate, DispycosNodeAllocate):
            return -1
        if not self._pulse_task:
            return -1
        if (node_allocate.__class__ != DispycosNodeAllocate and
            self._pulse_task.location != self.scheduler.location):
            node_allocate = copy.copy(node_allocate)
            node_allocate.__class__ = DispycosNodeAllocate
        return self.scheduler.send({'req': 'node_allocate', 'auth': self._auth,
                                    'node': node_allocate})

    def _run_request(self, request, where, cpu, gen, *args, **kwargs):
        """Internal use only.
        """
        if isinstance(gen, str):
            name = gen
        else:
            name = gen.__name__

        if name in self._xfer_funcs:
            code = None
        else:
            # if not inspect.isgeneratorfunction(gen):
            #     logger.warning('"%s" is not a valid generator function', name)
            #     raise StopIteration([])
            code = inspect.getsource(gen).lstrip()

        def _run_req(task=None):
            msg = {'req': 'job', 'auth': self._auth,
                   'job': _DispycosJob_(request, task, name, where, cpu, code, args, kwargs)}
            if (yield self.scheduler.deliver(msg, timeout=MsgTimeout)) == 1:
                reply = yield task.receive()
                if isinstance(reply, Task):
                    if self.status_task:
                        msg = DispycosTaskInfo(reply, args, kwargs, time.time())
                        self.status_task.send(DispycosStatus(Scheduler.TaskCreated, msg))
                if not request.endswith('async'):
                    reply = yield task.receive()
            else:
                reply = None
            raise StopIteration(reply)

        yield Task(_run_req).finish()

    def _pulse_proc(self, task=None):
        """For internal use only.
        """
        task.set_daemon()
        last_pulse = time.time()
        timeout = 2 * self._pulse_interval
        while 1:
            msg = yield task.receive(timeout=timeout)

            if msg == 'pulse':
                last_pulse = time.time()

            elif isinstance(msg, dict):
                if msg.get('auth', None) != self._auth:
                    continue
                if msg.get('req', None) == 'allocate':
                    reply = msg.get('reply', None)
                    args = msg.get('args', ())
                    if not isinstance(reply, Task) or not args:
                        logger.warning('Ignoring allocate request: %s', type(reply))
                        continue
                    ip_addr = args[0]
                    try:
                        node_allocation = self._node_allocations[int(msg['alloc_id'])]
                        assert re.match(node_allocation.ip_rex, ip_addr)
                        cpus = node_allocation.allocate(*args)
                    except Exception:
                        cpus = 0
                    reply.send({'auth': self._auth, 'req': 'allocate',
                                'ip_addr': ip_addr, 'cpus': cpus})

            elif msg == 'quit':
                break

            elif msg is None:
                logger.warning('scheduler may have gone away!')
                if (time.time() - last_pulse) > (10 * self._pulse_interval):
                    # TODO: inform status and / or "close"?
                    pass

            else:
                logger.debug('ignoring invalid pulse message')

        self._pulse_task = None

    def __getstate__(self):
        state = {}
        for attr in ['_code', '_xfer_funcs', '_xfer_files', '_auth',  'scheduler', 'status_task',
                     '_node_setup', '_server_setup', '_disable_nodes', '_disable_servers',
                     '_peers_communicate', '_pulse_interval', '_pulse_task', '_ping_interval',
                     '_zombie_period', '_abandon_zombie']:
            state[attr] = getattr(self, attr)
        if self._pulse_task.location == self.scheduler.location:
            node_allocations = self._node_allocations
        else:
            node_allocations = []
            for i in range(len(self._node_allocations)):
                obj = self._node_allocations[i]
                if obj.__class__ != DispycosNodeAllocate:
                    ip_rex = obj.ip_rex
                    obj = DispycosNodeAllocate('*', port=obj.port)
                    obj.ip_rex = ip_rex
                    obj.cpus = str(i)
                node_allocations.append(obj)
        state['_node_allocations'] = node_allocations
        return state

    def __setstate__(self, state):
        for attr, value in state.items():
            setattr(self, attr, value)


class _DispycosJob_(object):
    """Internal use only.
    """
    __slots__ = ('request', 'client', 'name', 'where', 'cpu', 'code', 'args', 'kwargs', 'done')

    def __init__(self, request, client, name, where, cpu, code, args=None, kwargs=None):
        self.request = request
        self.client = client
        self.name = name
        self.where = where
        self.cpu = cpu
        self.code = code
        self.args = pycos.serialize(args)
        self.kwargs = pycos.serialize(kwargs)
        self.done = None


class Scheduler(object, metaclass=pycos.Singleton):

    # status indications ('status' attribute of DispycosStatus)
    NodeDiscovered = 1
    NodeInitialized = 2
    NodeClosed = 3
    NodeIgnore = 4
    NodeDisconnected = 5
    NodeAbandoned = 6
    NodeSuspended = 7
    NodeResumed = 8

    ServerDiscovered = 11
    ServerInitialized = 12
    ServerClosed = 13
    ServerIgnore = 14
    ServerDisconnected = 15
    ServerAbandoned = 16
    ServerSuspended = 17
    ServerResumed = 18

    TaskCreated = 20
    TaskAbandoned = 21
    ComputationScheduled = 23
    ComputationClosed = 25

    """This class is for use by Computation class (see below) only.  Other than
    the status indications above, none of its attributes are to be accessed
    directly.
    """

    class _Node(object):

        def __init__(self, name, addr):
            self.name = name
            self.addr = addr
            self.cpus_used = 0
            self.cpus = 0
            self.platform = None
            self.avail_info = None
            self.servers = {}
            self.disabled_servers = {}
            self.load = 0.0
            self.status = Scheduler.NodeClosed
            self.task = None
            self.auth = None
            self.last_pulse = time.time()
            self.lock = pycos.Lock()
            self.cpu_avail = pycos.Event()
            self.cpu_avail.clear()
            self.abandon_zombie = False

    class _Server(object):

        def __init__(self, task, scheduler):
            self.task = task
            self.status = Scheduler.ServerClosed
            self.rtasks = {}
            self.xfer_files = []
            self.askew_results = {}
            self.cpu_avail = pycos.Event()
            self.cpu_avail.clear()
            self.scheduler = scheduler

        def run(self, job, computation, node):
            def _run(self, task=None):
                self.task.send({'req': 'run', 'auth': computation._auth, 'job': job, 'client': task})
                rtask = yield task.receive(timeout=MsgTimeout)
                # currently fault-tolerancy is not supported, so clear job's
                # args to save space
                job.args = job.kwargs = None
                if isinstance(rtask, Task):
                    # TODO: keep func too for fault-tolerance
                    job.done = pycos.Event()
                    self.rtasks[rtask] = (rtask, job)
                    if self.askew_results:
                        msg = self.askew_results.pop(rtask, None)
                        if msg:
                            self.scheduler.__status_task.send(msg)
                else:
                    logger.debug('failed to create rtask: %s', rtask)
                    if job.cpu:
                        self.cpu_avail.set()
                        if (self.status == Scheduler.ServerInitialized and
                            node.status == Scheduler.NodeInitialized):
                            node.cpu_avail.set()
                            self.scheduler._cpu_nodes.add(node)
                            self.scheduler._cpus_avail.set()
                            node.cpus_used -= 1
                            node.load = float(node.cpus_used) / len(node.servers)
                raise StopIteration(rtask)

            rtask = yield SysTask(_run, self).finish()
            job.client.send(rtask)

    def __init__(self, **kwargs):
        self._nodes = {}
        self._disabled_nodes = {}
        self._cpu_nodes = set()
        self._cpus_avail = pycos.Event()
        self._cpus_avail.clear()
        self._remote = False

        self._cur_computation = None
        self.__cur_client_auth = None
        self.__cur_node_allocations = []
        self.__pulse_interval = kwargs.pop('pulse_interval', MaxPulseInterval)
        self.__ping_interval = kwargs.pop('ping_interval', 0)
        self.__zombie_period = kwargs.pop('zombie_period', 100 * MaxPulseInterval)
        if not isinstance(pycos.config.DispycosSchedulerPort, int):
            pycos.config.DispycosSchedulerPort = eval(pycos.config.DispycosSchedulerPort)
        if not isinstance(pycos.config.DispycosNodePort, int):
            pycos.config.DispycosNodePort = eval(pycos.config.DispycosNodePort)
        self._node_port = pycos.config.DispycosNodePort
        self.__server_locations = set()

        kwargs['name'] = 'dispycos_scheduler'
        clean = kwargs.pop('clean', False)
        nodes = kwargs.pop('nodes', [])
        relay_nodes = kwargs.pop('relay_nodes', False)
        kwargs['udp_port'] = kwargs['tcp_port'] = pycos.config.DispycosSchedulerPort
        self.pycos = pycos.Pycos.instance(**kwargs)
        self.__dest_path = os.path.join(self.pycos.dest_path, 'dispycos', 'scheduler')
        if clean:
            shutil.rmtree(self.__dest_path)
        self.pycos.dest_path = self.__dest_path
        os.chmod(self.__dest_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

        self.__computation_sched_event = pycos.Event()
        self.__computation_scheduler_task = SysTask(self.__computation_scheduler_proc)
        self.__status_task = SysTask(self.__status_proc)
        self.__timer_task = SysTask(self.__timer_proc)
        self.__client_task = SysTask(self.__client_proc)
        self.__client_task.register('dispycos_scheduler')
        for node in nodes:
            if not isinstance(node, pycos.Location):
                node = pycos.Location(node, self._node_port)
            Task(self.pycos.peer, node, relay=relay_nodes)

    def status(self):
        pending_cpu = sum(node.cpus_used for node in self._nodes.values())
        pending = sum(len(server.rtasks) for node in self._nodes.values()
                      for server in node.servers.values())
        servers = functools.reduce(operator.add, [list(node.servers.keys())
                                                  for node in self._nodes.values()], [])
        return {'Client': self._cur_computation._pulse_task.location if self._cur_computation else '',
                'Pending': pending, 'PendingCPU': pending_cpu,
                'Nodes': list(self._nodes.keys()), 'Servers': servers
                }

    def print_status(self):
        status = self.status()
        print('')
        print('  Client: %s' % status['Client'])
        print('  Pending: %s' % status['Pending'])
        print('  Pending CPU: %s' % status['PendingCPU'])
        print('  nodes: %s' % len(status['Nodes']))
        print('  servers: %s' % len(status['Servers']))

    def __status_proc(self, task=None):
        task.set_daemon()
        task.register('dispycos_status')
        self.pycos.peer_status(self.__status_task)
        while 1:
            msg = yield task.receive()
            now = time.time()
            if isinstance(msg, pycos.MonitorException):
                rtask = msg.args[0]
                if not isinstance(rtask, Task):
                    logger.warning('ignoring invalid rtask %s', type(rtask))
                    continue
                node = self._nodes.get(rtask.location.addr, None)
                if not node:
                    node = self._disabled_nodes.get(rtask.location.addr, None)
                    if not node:
                        logger.warning('node %s is invalid', rtask.location.addr)
                        continue
                    if node.status == Scheduler.NodeAbandoned:
                        SysTask(self.__reclaim_node, node)

                server = node.servers.get(rtask.location, None)
                if not server:
                    server = node.disabled_servers.get(rtask.location, None)
                    if not server:
                        logger.warning('server "%s" is invalid', rtask.location)
                        continue
                node.last_pulse = now
                info = server.rtasks.pop(rtask, None)
                if not info:
                    # Due to 'yield' used to create rtask, scheduler may not
                    # have updated self._rtasks before the task's
                    # MonitorException is received, so put it in
                    # 'askew_results'. The scheduling task will resend it
                    # when it receives rtask
                    server.askew_results[rtask] = msg
                    continue
                # assert isinstance(info[1], _DispycosJob_)
                job = info[1]
                if job.cpu:
                    server.cpu_avail.set()
                    if (server.status == Scheduler.ServerInitialized and
                        node.status == Scheduler.NodeInitialized):
                        node.cpu_avail.set()
                        self._cpu_nodes.add(node)
                        self._cpus_avail.set()
                        node.cpus_used -= 1
                        node.load = float(node.cpus_used) / len(node.servers)
                if job.request.endswith('async'):
                    if job.done:
                        job.done.set()
                else:
                    job.client.send(msg.args[1][1])
                if self._cur_computation and self._cur_computation.status_task:
                    if len(msg.args) > 2:
                        msg.args = (msg.args[0], msg.args[1])
                    self._cur_computation.status_task.send(msg)

            elif isinstance(msg, pycos.PeerStatus):
                if msg.status == pycos.PeerStatus.Online:
                    if msg.name.endswith('_server-0'):
                        SysTask(self.__discover_node, msg)
                else:
                    # msg.status == pycos.PeerStatus.Offline
                    node = server = None
                    node = self._nodes.get(msg.location.addr, None)
                    if not node:
                        node = self._disabled_nodes.get(msg.location.addr, None)
                    if node:
                        server = node.servers.pop(msg.location, None)
                        if server:
                            if node.servers:
                                node.disabled_servers[msg.location] = server
                        else:
                            server = node.disabled_servers.get(msg.location, None)

                        if server:
                            server.status = Scheduler.ServerDisconnected
                            SysTask(self.__close_server, server, node)
                        elif node.task and node.task.location == msg.location:
                            # TODO: inform scheduler / client
                            if not self._nodes.pop(node.addr, None):
                                self._disabled_nodes.get(node.addr, None)
                            node.status = Scheduler.NodeDisconnected
                            SysTask(self.__close_node, node)

                    if ((not server and not node) and self._remote and self._cur_computation and
                        self._cur_computation._pulse_task.location == msg.location):
                        logger.warning('Client %s terminated; closing computation %s',
                                       msg.location, self.__cur_client_auth)
                        SysTask(self.__close_computation)

            elif isinstance(msg, dict):  # message from a node's server
                status = msg.get('status', None)
                if status == 'pulse':
                    location = msg.get('location', None)
                    if not isinstance(location, pycos.Location):
                        continue
                    node = self._nodes.get(location.addr, None)
                    if node:
                        node.last_pulse = now
                        node_status = msg.get('node_status', None)
                        if (node_status and self._cur_computation and
                           self._cur_computation.status_task):
                            self._cur_computation.status_task.send(node_status)
                    else:
                        node = self._disabled_nodes.get(location.addr, None)
                        if node and node.status == Scheduler.NodeAbandoned:
                            SysTask(self.__reclaim_node, node)

                elif status == Scheduler.ServerDiscovered:
                    rtask = msg.get('task', None)
                    if not isinstance(rtask, pycos.Task):
                        continue
                    if (not self._cur_computation or
                        self._cur_computation._auth != msg.get('auth', None)):
                        continue
                    node = self._nodes.get(rtask.location.addr, None)
                    if not node:
                        node = self._disabled_nodes.get(rtask.location.addr, None)
                    if not node or (node.status != Scheduler.NodeInitialized and
                                    node.status != Scheduler.NodeDiscovered and
                                    node.status != Scheduler.NodeSuspended):
                        if node:
                            logger.warning('Node at %s is not initialized for server %s: %s',
                                           node.addr, rtask.location, node.status)
                        else:
                            logger.warning('Node is not valid for server %s', rtask.location)
                        continue
                    if (not self._cur_computation or
                        self._cur_computation._auth != msg.get('auth', None)):
                        logger.warning('Status %s for server %s is ignored', status, rtask.location)
                        continue
                    server = node.servers.get(rtask.location, None)
                    if server:
                        continue
                    server = Scheduler._Server(rtask, self)
                    server.status = Scheduler.ServerDiscovered
                    node.disabled_servers[rtask.location] = server
                    if self._cur_computation and self._cur_computation.status_task:
                        info = DispycosStatus(server.status, server.task.location)
                        self._cur_computation.status_task.send(info)

                elif status == Scheduler.ServerInitialized:
                    rtask = msg.get('task', None)
                    if not isinstance(rtask, pycos.Task):
                        continue
                    if (not self._cur_computation or
                        self._cur_computation._auth != msg.get('auth', None)):
                        continue
                    node = self._nodes.get(rtask.location.addr, None)
                    if not node:
                        node = self._disabled_nodes.get(rtask.location.addr, None)
                    if not node or (node.status != Scheduler.NodeInitialized and
                                    node.status != Scheduler.NodeDiscovered and
                                    node.status != Scheduler.NodeSuspended):
                        if node:
                            logger.warning('Node at %s is not initialized for server %s: %s',
                                           node.addr, rtask.location, node.status)
                        else:
                            logger.warning('Node is not valid for server %s', rtask.location)
                        continue
                    if (not self._cur_computation or
                        self._cur_computation._auth != msg.get('auth', None)):
                        logger.warning('Status %s for server %s is ignored', status, rtask.location)
                        continue
                    server = node.disabled_servers.pop(rtask.location, None)
                    if server:
                        if (server.status != Scheduler.ServerDiscovered and
                            server.status != Scheduler.ServerSuspended):
                            continue
                    else:
                        server = Scheduler._Server(rtask, self)

                    node.last_pulse = now
                    server.status = Scheduler.ServerInitialized
                    if node.status == Scheduler.NodeInitialized:
                        if not node.servers:
                            if self._cur_computation and self._cur_computation.status_task:
                                info = DispycosNodeInfo(node.name, node.addr, node.cpus,
                                                        node.platform, node.avail_info)
                                info = DispycosStatus(node.status, info)
                                self._cur_computation.status_task.send(info)
                            self._disabled_nodes.pop(rtask.location.addr, None)
                            self._nodes[rtask.location.addr] = node
                        node.servers[rtask.location] = server
                        server.cpu_avail.set()
                        self._cpu_nodes.add(node)
                        self._cpus_avail.set()
                        node.cpu_avail.set()
                        node.load = float(node.cpus_used) / len(node.servers)
                        if self._cur_computation and self._cur_computation.status_task:
                            self._cur_computation.status_task.send(
                                DispycosStatus(server.status, server.task.location))
                    else:
                        node.disabled_servers[rtask.location] = server

                    if self._cur_computation._peers_communicate:
                        server.task.send({'req': 'peers', 'auth': self._cur_computation._auth,
                                          'peers': list(self.__server_locations)})
                        self.__server_locations.add(server.task.location)

                elif status in (Scheduler.ServerClosed, Scheduler.ServerDisconnected):
                    location = msg.get('location', None)
                    if not isinstance(location, pycos.Location):
                        continue
                    node = self._nodes.get(location.addr, None)
                    if not node:
                        node = self._disabled_nodes.get(location.addr, None)
                        if not node:
                            continue
                    if (not self._cur_computation or
                        self._cur_computation._auth != msg.get('auth', None)):
                        logger.warning('Status %s for server %s is ignored', status, rtask.location)
                        continue
                    server = node.servers.pop(location, None)
                    if not server:
                        server = node.disabled_servers.get(location, None)
                        if not server:
                            continue
                        if status == Scheduler.ServerDisconnected:
                            server.status = status
                            SysTask(self.__close_server, server, node)
                    server.status = Scheduler.ServerClosed
                    node.disabled_servers[location] = server
                    if not node.servers:
                        node.status = Scheduler.NodeClosed
                        self._nodes.pop(node.addr, None)
                        self._disabled_nodes[location.addr] = node
                        self._cpu_nodes.discard(node)
                        if not self._cpu_nodes:
                            self._cpus_avail.clear()
                    if self._cur_computation:
                        if self._cur_computation._peers_communicate:
                            self.__server_locations.discard(server.task.location)
                            # TODO: inform other servers
                            # if not node.servers:
                            #     info = DispycosNodeInfo(node.name, node.addr, node.cpus,
                            #                            node.platform, node.avail_info)
                            #     self._cur_computation.status_task.send(
                            #         Scheduler.NodeClosed, DispycosStatus(node.status, info))

                elif status == Scheduler.NodeClosed:
                    location = msg.get('location', None)
                    if not isinstance(location, pycos.Location):
                        continue
                    node = self._nodes.pop(location.addr, None)
                    if not node:
                        node = self._disabled_nodes.get(location.addr, None)
                        if not node:
                            continue
                    if (not self._cur_computation or
                        self._cur_computation._auth != msg.get('auth', None)):
                        logger.warning('Status %s for node %s is ignored', status, location)
                        continue
                    node.status = Scheduler.NodeDisconnected
                    SysTask(self.__close_node, node)

                else:
                    logger.warning('Ignoring invalid status message: %s', status)
            else:
                logger.warning('invalid status message ignored')

    def __node_allocate(self, node, task=None):
        if not task:
            task = pycos.Pycos.cur_task()
        for node_allocate in self.__cur_node_allocations:
            if not re.match(node_allocate.ip_rex, node.addr):
                continue
            if self._remote and isinstance(node_allocate.cpus, str):
                req = {'req': 'allocate', 'auth': self.__cur_client_auth,
                       'alloc_id': node_allocate.cpus, 'reply': task,
                       'args': (node.addr, node.name, node.platform, node.cpus,
                                node.avail_info.memory, node.avail_info.disk)}
                self._cur_computation._pulse_task.send(req)
                reply = yield task.recv(timeout=MsgTimeout)
                if (isinstance(reply, dict) and reply.get('auth', None) == self.__cur_client_auth and
                    reply.get('req', None) == 'allocate' and reply.get('ip_addr', '') == node.addr):
                    cpus = reply.get('cpus', 0)
                else:
                    cpus = 0
            else:
                cpus = node_allocate.allocate(node.addr, node.name, node.platform, node.cpus,
                                              node.avail_info.memory, node.avail_info.disk)
            if cpus < 0:
                continue
            raise StopIteration(min(cpus, node.cpus))
        raise StopIteration(node.cpus)

    def __get_node_info(self, node, task=None):
        assert node.addr in self._disabled_nodes
        node.task.send({'req': 'dispycos_node_info', 'client': task})
        node_info = yield task.receive(timeout=MsgTimeout)
        if not node_info:
            node.status = Scheduler.NodeIgnore
            raise StopIteration
        node.name = node_info.name
        node.cpus = node_info.cpus
        node.platform = node_info.platform.lower()
        node.avail_info = node_info.avail_info
        if self._cur_computation:
            yield self.__init_node(node, task=task)

    def __init_node(self, node, setup_args=(), task=None):
        computation = self._cur_computation
        if not computation or not node.task:
            raise StopIteration(-1)
        # this task may be invoked in two different paths (when a node is
        # found right after computation is already scheduled, and when
        # computation is scheduled right after a node is found). To prevent
        # concurrent execution (that may reserve / initialize same node more
        # than once), lock is used
        yield node.lock.acquire()
        # assert node.addr in self._disabled_nodes
        if node.status not in (Scheduler.NodeDiscovered, Scheduler.NodeClosed):
            logger.warning('Ignoring node initialization for %s: %s', node.addr, node.status)
            node.lock.release()
            raise StopIteration(0)

        if node.status == Scheduler.NodeClosed:
            cpus = yield self.__node_allocate(node, task=task)
            if not cpus:
                node.status = Scheduler.NodeIgnore
                node.lock.release()
                raise StopIteration(0)

            node.task.send({'req': 'reserve', 'cpus': cpus, 'auth': computation._auth,
                            'status_task': self.__status_task, 'client': task,
                            'computation_location': computation._pulse_task.location,
                            'abandon_zombie': computation._abandon_zombie})
            reply = yield task.receive(timeout=MsgTimeout)
            if not isinstance(reply, dict) or reply.get('cpus', 0) <= 0:
                logger.debug('Reserving %s failed', node.addr)
                self._disabled_nodes.pop(node.addr, None)
                # node.status = Scheduler.NodeDiscoverd
                node.lock.release()
                yield pycos.Pycos.instance().close_peer(node.task.location)
                raise StopIteration(-1)
            if computation != self._cur_computation:
                node.status = Scheduler.NodeClosed
                node.task.send({'req': 'release', 'auth': computation._auth, 'client': None})
                node.lock.release()
                raise StopIteration(-1)

            node.status = Scheduler.NodeDiscovered
            node.cpus = reply['cpus']
            node.auth = reply.get('auth', None)
            if self._cur_computation and self._cur_computation.status_task:
                info = DispycosNodeInfo(node.name, node.addr, node.cpus, node.platform,
                                        node.avail_info)
                self._cur_computation.status_task.send(DispycosStatus(node.status, info))

            if self._cur_computation._disable_nodes:
                node.lock.release()
                raise StopIteration(0)
        else:
            assert node.addr in self._disabled_nodes

        for name, dst, sep in computation._xfer_files:
            reply = yield self.pycos.send_file(node.task.location, name, dir=dst, timeout=MsgTimeout,
                                               overwrite=True)
            if reply < 0 or computation != self._cur_computation:
                logger.debug('Failed to transfer file %s: %s', name, reply)
                node.status = Scheduler.NodeClosed
                node.task.send({'req': 'release', 'auth': computation._auth, 'client': None})
                node.lock.release()
                raise StopIteration(-1)

        node.task.send({'req': 'computation', 'computation': computation, 'auth': computation._auth,
                        'setup_args': setup_args, 'client': task})
        cpus = yield task.receive(timeout=MsgTimeout)
        if not cpus or computation != self._cur_computation:
            node.status = Scheduler.NodeClosed
            node.task.send({'req': 'release', 'auth': computation._auth, 'client': None})
            node.lock.release()
            raise StopIteration(-1)

        node.cpus = cpus
        node.status = Scheduler.NodeInitialized
        node.lock.release()
        servers = [server for server in node.disabled_servers.values()
                   if server.status == Scheduler.ServerInitialized]
        if servers:
            if computation.status_task:
                info = DispycosNodeInfo(node.name, node.addr, node.cpus, node.platform,
                                        node.avail_info)
                computation.status_task.send(DispycosStatus(node.status, info))
            self._disabled_nodes.pop(node.addr, None)
            self._nodes[node.addr] = node
            node.cpu_avail.set()
            self._cpu_nodes.add(node)
            self._cpus_avail.set()
            for server in servers:
                node.disabled_servers.pop(server.task.location)
                node.servers[server.task.location] = server
                server.cpu_avail.set()
                if computation.status_task:
                    computation.status_task.send(DispycosStatus(server.status,
                                                                server.task.location))

    def __discover_node(self, peer_status, task=None):
        for _ in range(10):
            node_task = yield Task.locate('dispycos_node', location=peer_status.location,
                                          timeout=MsgTimeout)
            if not isinstance(node_task, Task):
                yield task.sleep(0.1)
                continue
            node = self._nodes.pop(peer_status.location.addr, None)
            if not node:
                node = self._disabled_nodes.pop(peer_status.location.addr, None)
            if node:
                logger.warning('Rediscovered dispycosnode at %s', peer_status.location.addr)
                if node_task == node.task and node.status == Scheduler.NodeAbandoned:
                    SysTask(self.__reclaim_node, node)
                    raise StopIteration
                node.status = Scheduler.NodeDisconnected
                yield SysTask(self.__close_node, node).finish()
            node = Scheduler._Node(peer_status.name, peer_status.location.addr)
            self._disabled_nodes[peer_status.location.addr] = node
            node.task = node_task
            yield self.__get_node_info(node, task=task)
            raise StopIteration

    def __reclaim_node(self, node, task=None):
        node.task.send({'req': 'status', 'status_task': self.__status_task, 'client': task,
                        'auth': node.auth})
        status = yield task.recv(timeout=MsgTimeout)
        if not isinstance(status, dict):
            logger.debug('dispycosnode %s is used by another scheduler', node.addr)
            raise StopIteration(-1)
        self._disabled_nodes.pop(node.addr, None)
        node.disabled_servers.update(node.servers)
        node.servers.clear()
        computation = self._cur_computation
        if computation and computation._auth == status.get('computation_auth'):
            for rtask in status.get('servers', []):
                server = node.disabled_servers.pop(rtask.location, None)
                if not server:
                    logger.warning('Invalid server %s ignored', rtask)
                    continue
                # TODO: get number of CPU jobs only
                server.task.send({'req': 'num_jobs', 'auth': computation._auth, 'client': task})
                n = yield task.receive(timeout=MsgTimeout)
                if not isinstance(n, int):
                    continue
                if n == 0:
                    server.cpu_avail.set()
                else:
                    server.cpu_avail.clear()
                server.status = Scheduler.ServerInitialized
                node.servers[rtask.location] = server
            node.status = Scheduler.NodeInitialized
            node.last_pulse = time.time()
            if any(server.cpu_avail.is_set() for server in node.servers.values()):
                node.cpu_avail.set()
                self._cpu_nodes.add(node)
                self._cpus_avail.set()
            self._nodes[node.addr] = node
            logger.debug('Rediscovered node %s with %s servers', node.addr, len(node.servers))
            raise StopIteration

        node.status = Scheduler.NodeDisconnected
        yield SysTask(self.__close_node, node).finish()
        self._disabled_nodes[node.addr] = node
        yield self.__get_node_info(node, task=task)
        raise StopIteration

    def __timer_proc(self, task=None):
        task.set_daemon()
        node_check = client_pulse = last_ping = time.time()
        while 1:
            try:
                yield task.sleep(self.__pulse_interval)
            except GeneratorExit:
                break
            now = time.time()
            if self.__cur_client_auth:
                if (yield self._cur_computation._pulse_task.deliver('pulse')) == 1:
                    client_pulse = now
                if self.__zombie_period:
                    if ((now - client_pulse) > self.__zombie_period):
                        logger.warning('Closing zombie computation %s', self.__cur_client_auth)
                        SysTask(self.__close_computation)

                    if (now - node_check) > self.__zombie_period:
                        node_check = now
                        for node in list(self._nodes.values()):
                            if (node.status != Scheduler.NodeInitialized and
                                node.status != Scheduler.NodeDiscovered and
                                node.status != Scheduler.NodeSuspended):
                                continue
                            if (now - node.last_pulse) > self.__zombie_period:
                                logger.warning('dispycos node %s is zombie!', node.addr)
                                self._nodes.pop(node.addr, None)
                                self._disabled_nodes[node.addr] = node
                                # TODO: assuming servers are zombies as well
                                node.status = Scheduler.NodeAbandoned
                                SysTask(self.__close_node, node)

                        if not self._cur_computation._disable_nodes:
                            for node in self._disabled_nodes.values():
                                if node.task and node.status == Scheduler.NodeDiscovered:
                                    SysTask(self.__init_node, node)

            if self.__ping_interval and ((now - last_ping) > self.__ping_interval):
                last_ping = now
                if not self.pycos.ignore_peers:
                    self.pycos.discover_peers(port=self._node_port)

    def __computation_scheduler_proc(self, task=None):
        task.set_daemon()
        while 1:
            if self._cur_computation:
                self.__computation_sched_event.clear()
                yield self.__computation_sched_event.wait()
                continue

            self._cur_computation, client = yield task.receive()
            self.__pulse_interval = self._cur_computation._pulse_interval
            self.__ping_interval = self._cur_computation._ping_interval
            if not self._remote:
                self.__zombie_period = self._cur_computation._zombie_period

            self.__cur_client_auth = self._cur_computation._auth
            self._cur_computation._auth = hashlib.sha1(os.urandom(20)).hexdigest()
            self.__cur_node_allocations = self._cur_computation._node_allocations
            self._cur_computation._node_allocations = []

            self._disabled_nodes.update(self._nodes)
            self._nodes.clear()
            self._cpu_nodes.clear()
            self._cpus_avail.clear()
            for node in self._disabled_nodes.values():
                node.status = Scheduler.NodeClosed
                node.disabled_servers.clear()
                node.servers.clear()
                node.cpu_avail.clear()
            logger.debug('Computation %s / %s scheduled', self.__cur_client_auth,
                         self._cur_computation._auth)
            msg = {'resp': 'scheduled', 'auth': self.__cur_client_auth}
            if (yield client.deliver(msg, timeout=MsgTimeout)) != 1:
                logger.warning('client not reachable?')
                self._cur_client_auth = None
                self._cur_computation = None
                continue
            for node in self.__cur_node_allocations:
                if node.ip_rex.find('*') >= 0:
                    continue
                loc = pycos.Location(node.ip_rex.replace('\\.', '.'),
                                     node.port if node.port else self._node_port)
                SysTask(self.pycos.peer, loc)
            for node in self._disabled_nodes.values():
                SysTask(self.__get_node_info, node)
            if not self.pycos.ignore_peers:
                self.pycos.discover_peers(port=self._node_port)
            self.__timer_task.resume()
        self.__computation_scheduler_task = None

    def __submit_job(self, msg, task=None):
        task.set_daemon()
        job = msg['job']
        auth = msg.get('auth', None)
        if (not isinstance(job, _DispycosJob_) or not isinstance(job.client, Task)):
            logger.warning('Ignoring invalid client job request: %s' % type(job))
            raise StopIteration
        cpu = job.cpu
        where = job.where
        if not where:
            while 1:
                node = None
                load = None
                if cpu:
                    for host in self._cpu_nodes:
                        if host.cpu_avail.is_set() and (load is None or host.load < load):
                            node = host
                            load = host.load
                else:
                    for host in self._nodes.values():
                        if load is None or host.load < load:
                            node = host
                            load = host.load
                if not node:
                    self._cpus_avail.clear()
                    yield self._cpus_avail.wait()
                    if self.__cur_client_auth != auth:
                        raise StopIteration
                    continue
                server = None
                load = None
                for proc in node.servers.values():
                    if cpu:
                        if proc.cpu_avail.is_set() and (load is None or len(proc.rtasks) < load):
                            server = proc
                            load = len(proc.rtasks)
                    elif (load is None or len(proc.rtasks) < load):
                        server = proc
                        load = len(proc.rtasks)
                if server:
                    break
                else:
                    self._cpus_avail.clear()
                    yield self._cpus_avail.wait()
                    if self.__cur_client_auth != auth:
                        raise StopIteration
                    continue

            if cpu:
                server.cpu_avail.clear()
                node.cpus_used += 1
                node.load = float(node.cpus_used) / len(node.servers)
                if node.cpus_used == len(node.servers):
                    node.cpu_avail.clear()
                    self._cpu_nodes.discard(node)
                    if not self._cpu_nodes:
                        self._cpus_avail.clear()
            yield server.run(job, self._cur_computation, node)

        elif isinstance(where, str):
            node = self._nodes.get(where, None)
            if not node:
                job.client.send(None)
                raise StopIteration
            while 1:
                server = None
                load = None
                for proc in node.servers.values():
                    if cpu:
                        if proc.cpu_avail.is_set() and (load is None or len(proc.rtasks) < load):
                            server = proc
                            load = len(proc.rtasks)
                    elif (load is None or len(proc.rtasks) < load):
                        server = proc
                        load = len(proc.rtasks)

                if server:
                    break
                else:
                    yield node.cpu_avail.wait()
                    if self.__cur_client_auth != auth:
                        raise StopIteration
                    continue

            if cpu:
                server.cpu_avail.clear()
                node.cpus_used += 1
                node.load = float(node.cpus_used) / len(node.servers)
                if node.cpus_used >= len(node.servers):
                    node.cpu_avail.clear()
                    self._cpu_nodes.discard(node)
                    if not self._cpu_nodes:
                        self._cpus_avail.clear()
            yield server.run(job, self._cur_computation, node)

        elif isinstance(where, pycos.Location):
            node = self._nodes.get(where.addr)
            if not node:
                job.client.send(None)
                raise StopIteration
            server = node.servers.get(where)
            if not server:
                job.client.send(None)
                raise StopIteration
            if cpu:
                while (not node.cpu_avail.is_set() or not server.cpu_avail.is_set()):
                    yield server.cpu_avail.wait()
                    if self.__cur_client_auth != auth:
                        raise StopIteration
                server.cpu_avail.clear()
                node.cpus_used += 1
                node.load = float(node.cpus_used) / len(node.servers)
                if node.cpus_used >= len(node.servers):
                    node.cpu_avail.clear()
                    self._cpu_nodes.discard(node)
                    if not self._cpu_nodes:
                        self._cpus_avail.clear()
            yield server.run(job, self._cur_computation, node)

        else:
            job.client.send(None)

    def __client_proc(self, task=None):
        task.set_daemon()
        computations = {}

        while 1:
            msg = yield task.receive()
            if not isinstance(msg, dict):
                continue
            req = msg.get('req', None)
            auth = msg.get('auth', None)
            if self.__cur_client_auth != auth:
                if req == 'schedule' or req == 'await':
                    pass
                else:
                    continue

            if req == 'job':
                SysTask(self.__submit_job, msg)
                continue

            client = msg.get('client', None)
            if not isinstance(client, pycos.Task):
                client = None

            if req == 'enable_server':
                loc = msg.get('server', None)
                if not isinstance(loc, pycos.Location):
                    continue
                node = self._nodes.get(loc.addr, None)
                if not node:
                    node = self._disabled_nodes.get(loc.addr, None)
                if not node or node.status not in (Scheduler.NodeInitialized,
                                                   Scheduler.NodeSuspended):
                    continue
                server = node.disabled_servers.get(loc, None)
                if not server or server.status not in (Scheduler.ServerDiscovered,
                                                       Scheduler.ServerSuspended):
                    continue
                if server.status == Scheduler.ServerDiscovered:
                    args = msg.get('setup_args', ())
                    server.task.send({'req': 'enable_server', 'setup_args': args,
                                      'auth': self._cur_computation._auth})
                elif server.status == Scheduler.ServerSuspended:
                    node.disabled_servers.pop(loc)
                    node.servers[loc] = server
                    server.status = Scheduler.ServerInitialized
                    server.cpu_avail.set()
                    if len(node.servers) == 1:
                        node.cpu_avail.set()
                        self._cpu_nodes.add(node)
                        self._cpus_avail.set()
                    if self._cur_computation.status_task:
                        info = DispycosStatus(Scheduler.ServerResumed, loc)
                        self._cur_computation.status_task.send(info)
                    if node.status == Scheduler.NodeSuspended:
                        self._disabled_nodes.pop(node.addr, None)
                        self._nodes[node.addr] = node
                        node.status = Scheduler.NodeInitialized
                        if self._cur_computation.status_task:
                            info = DispycosNodeInfo(node.name, node.addr, node.cpus, node.platform,
                                                    node.avail_info)
                            info = DispycosStatus(Scheduler.NodeResumed, info)
                            self._cur_computation.status_task.send(info)

            elif req == 'enable_node':
                addr = msg.get('addr', None)
                if not addr:
                    continue
                node = self._disabled_nodes.get(addr, None)
                if not node or node.status not in (Scheduler.NodeDiscovered,
                                                   Scheduler.NodeSuspended):
                    continue
                if node.status == Scheduler.NodeDiscovered:
                    setup_args = msg.get('setup_args', ())
                    SysTask(self.__init_node, node, setup_args=setup_args)
                elif node.status == Scheduler.NodeSuspended:
                    if node.servers:
                        node.status = Scheduler.NodeInitialized
                        self._disabled_nodes.pop(addr, None)
                        self._nodes[node.addr] = node
                        node.cpu_avail.set()
                        self._cpu_nodes.add(node)
                        self._cpus_avail.set()
                        if self._cur_computation.status_task:
                            info = DispycosNodeInfo(node.name, node.addr, node.cpus, node.platform,
                                                    node.avail_info)
                            info = DispycosStatus(Scheduler.NodeResumed, info)
                            self._cur_computation.status_task.send(info)

            elif req == 'suspend_server':
                loc = msg.get('server', None)
                if not isinstance(loc, pycos.Location):
                    continue
                node = self._nodes.get(loc.addr, None)
                if not node:
                    continue
                server = node.servers.pop(loc, None)
                if not server:
                    continue
                if server.status not in (Scheduler.ServerInitialized, Scheduler.ServerDiscovered):
                    node.servers[loc] = server
                    continue
                node.disabled_servers[loc] = server
                if server.status == Scheduler.ServerInitialized:
                    server.status = Scheduler.ServerSuspended
                server.cpu_avail.clear()
                if self._cur_computation.status_task:
                    info = DispycosStatus(server.status, loc)
                    self._cur_computation.status_task.send(info)
                if not node.servers:
                    self._nodes.pop(node.addr)
                    self._disabled_nodes[node.addr] = node
                    node.status = Scheduler.NodeSuspended
                    node.cpu_avail.clear()
                    self._cpu_nodes.discard(node)
                    if not self._cpu_nodes:
                        self._cpus_avail.clear()
                    if self._cur_computation.status_task:
                        info = DispycosNodeInfo(node.name, node.addr, node.cpus, node.platform,
                                                node.avail_info)
                        info = DispycosStatus(node.status, info)
                        self._cur_computation.status_task.send(info)

            elif req == 'suspend_node':
                addr = msg.get('addr', None)
                if not addr:
                    continue
                node = self._nodes.pop(addr, None)
                if not node:
                    continue
                if node.status not in (Scheduler.NodeInitialized, Scheduler.NodeDiscovered):
                    self._nodes[addr] = node
                    continue
                self._disabled_nodes[node.addr] = node
                if node.status == Scheduler.NodeInitialized:
                    node.status = Scheduler.NodeSuspended
                node.cpu_avail.clear()
                self._cpu_nodes.discard(node)
                if not self._cpu_nodes:
                    self._cpus_avail.clear()
                if self._cur_computation.status_task:
                    info = DispycosNodeInfo(node.name, node.addr, node.cpus, node.platform,
                                            node.avail_info)
                    info = DispycosStatus(node.status, info)
                    self._cur_computation.status_task.send(info)

            elif req == 'abandon_zombie':
                addr = msg.get('addr', None)
                if not addr:
                    if self._cur_computation:
                        if self._cur_computation.abandon_zombie == bool(msg.get('flag', False)):
                            continue
                        self._cur_computation.abandon_zombie = bool(msg.get('flag', False))
                        req = {'req': 'abandon_zombie', 'auth': self._cur_computation._auth,
                               'flag': bool(msg.get('flag', False))}
                        for node in self._nodes.values():
                            if node.task:
                                req['node_auth'] = node.auth
                                node.task.send(req)
                    continue
                node = self._nodes.get(addr, None)
                if node:
                    node.abandon_zombie = msg.get('flag')
                    if node.task and self._cur_computation:
                        node.task.send({'req': 'abandon_zombie', 'node_auth': node.auth,
                                        'auth': self._cur_computation._auth})

            elif req == 'close_node':
                addr = msg.get('addr', None)
                if not addr:
                    continue
                node = self._nodes.pop(addr, None)
                if not node:
                    continue
                self._disabled_nodes[node.addr] = node
                if node.task and self._cur_computation:
                    req = {'req': 'release', 'node_auth': node.auth,
                           'auth': self._cur_computation._auth,
                           'terminate': msg.get('terminate', False)}
                    node.task.send(req)

            elif req == 'node_allocate':
                node = req.get('node', None)
                if not isinstance(node, DispycosNodeAllocate):
                    continue
                self.__cur_node_allocations = [node] + [na for na in self.__cur_node_allocations
                                                        if na.ip_rex != node.ip_rex]
                if node.ip_rex.find('*') >= 0:
                    continue
                loc = pycos.Location(node.ip_rex.replace('\\.', '.'),
                                     node.port if node.port else self._node_port)
                SysTask(self.pycos.peer, loc)

            elif req == 'nodes':
                if isinstance(client, Task):
                    nodes = [node.addr for node in self._nodes.values()
                             if node.status == Scheduler.NodeInitialized]
                    client.send(nodes)

            elif req == 'servers':
                if isinstance(client, Task):
                    servers = [server.task.location for node in self._nodes.values()
                               if node.status == Scheduler.NodeInitialized
                               for server in node.servers.values()
                               # if server.status == Scheduler.ServerInitialized
                               ]
                    client.send(servers)

            elif req == 'tasks':
                servers = []
                tasks = []
                where = msg.get('at', None)
                if where:
                    if isinstance(where, pycos.Location):
                        addr = where.addr
                    else:
                        addr = where
                    node = self._nodes.get(addr, None)
                    if not node:
                        node = self._disabled_nodes.get(addr, None)
                    if node:
                        if isinstance(where, pycos.Location):
                            server = node.servers.get(where, None)
                            if not server:
                                server = node.disabled_servers.get(where, None)
                            if server:
                                servers = [server]
                        else:
                            servers.extend(node.servers.values())
                            servers.extend(node.disabled_servers.values())

                else:
                    for node in self._nodes.values():
                        servers.extend(node.servers.values())
                        servers.extend(node.disabled_servers.values())

                for server in servers:
                    tasks.extend(server.rtasks.keys())
                if isinstance(client, Task):
                    client.send(tasks)

            elif req == 'schedule':
                if not isinstance(client, Task):
                    logger.warning('Ignoring invalid client request "%s"', req)
                    continue
                try:
                    computation = pycos.deserialize(msg['computation'])
                    assert isinstance(computation, Computation) or \
                        computation.__class__.__name__ == 'Computation'
                    assert isinstance(computation._pulse_task, Task)
                    if computation._pulse_task.location == self.pycos.location:
                        computation._pulse_task._id = int(computation._pulse_task._id)
                        if computation.status_task:
                            computation.status_task._id = int(computation.status_task._id)
                    assert isinstance(computation._pulse_interval, (float, int))
                    assert (MinPulseInterval <= computation._pulse_interval <= MaxPulseInterval)
                except Exception:
                    logger.warning('ignoring invalid computation request')
                    client.send(None)
                    continue
                while 1:
                    computation._auth = hashlib.sha1(os.urandom(20)).hexdigest()
                    if not os.path.exists(os.path.join(self.__dest_path, computation._auth)):
                        break
                try:
                    os.mkdir(os.path.join(self.__dest_path, computation._auth))
                except Exception:
                    logger.debug('Could not create "%s"',
                                 os.path.join(self.__dest_path, computation._auth))
                    client.send(None)
                    continue
                # TODO: save it on disk instead
                computations[computation._auth] = computation
                client.send(computation._auth)

            elif req == 'await':
                if not isinstance(client, Task):
                    logger.warning('Ignoring invalid client request "%s"', req)
                    continue
                computation = computations.pop(auth, None)
                if not computation:
                    client.send(None)
                    continue
                if computation._pulse_task.location.addr != self.pycos.location.addr:
                    computation._xfer_files = [(os.path.join(self.__dest_path, computation._auth,
                                                             os.path.join(*(dst.split(sep))),
                                                             xf.split(sep)[-1]),
                                                os.path.join(*(dst.split(sep))), os.sep)
                                               for xf, dst, sep in computation._xfer_files]
                for xf, dst, sep in computation._xfer_files:
                    if not os.path.isfile(xf):
                        logger.warning('File "%s" for computation %s is not valid',
                                       xf, computation._auth)
                        computation = None
                        break
                if computation is None:
                    client.send(None)
                else:
                    self.__computation_scheduler_task.send((computation, client))
                    self.__computation_sched_event.set()

            elif req == 'close_computation':
                if not isinstance(client, Task):
                    logger.warning('Ignoring invalid client request "%s"', req)
                    continue
                SysTask(self.__close_computation, client=client,
                        await_async=msg.get('await_async', False))

            else:
                logger.warning('Ignoring invalid client request "%s"', req)

    def __close_node(self, node, await_async=False, task=None):
        if not node.task:
            logger.debug('Closing node %s ignored: %s', node.addr, node.status)
            raise StopIteration(-1)

        node.cpu_avail.clear()
        self._cpu_nodes.discard(node)
        if not self._cpu_nodes:
            self._cpus_avail.clear()
        self._nodes.pop(node.addr, None)
        self._disabled_nodes[node.addr] = node
        node.disabled_servers.update(node.servers)
        node.servers.clear()
        computation = self._cur_computation
        status_info = DispycosNodeInfo(node.name, node.addr, node.cpus, node.platform,
                                       node.avail_info)
        if node.status == Scheduler.NodeAbandoned:
            # TODO: safe to assume servers are disconnected as well?
            for server in node.disabled_servers.values():
                if server.task:
                    server.status = Scheduler.ServerAbandoned

        close_tasks = [SysTask(self.__close_server, server, node, await_async=await_async)
                       for server in node.disabled_servers.values() if server.task]
        for close_task in close_tasks:
            yield close_task.finish()
        if (computation and computation.status_task):
            computation.status_task.send(DispycosStatus(node.status, status_info))
        if ((node.status == Scheduler.NodeDisconnected) or
            (node.status == Scheduler.NodeAbandoned and node.abandon_zombie)):
            self._disabled_nodes.pop(node.addr, None)
            # TODO: it is not safe to throw away peer if node is still running
            Task(pycos.Pycos.instance().close_peer, node.task.location, timeout=2)
        if node.task and node.status not in [Scheduler.NodeAbandoned, Scheduler.NodeDisconnected]:
            node.task.send({'req': 'release', 'auth': computation._auth, 'node_auth': node.auth})

    def __close_server(self, server, node, await_async=False, task=None):
        if not server.task:
            raise StopIteration(-1)
        computation = self._cur_computation
        if computation:
            status_task = computation.status_task
        else:
            status_task = None

        if node.servers.pop(server.task.location, None):
            node.disabled_servers[server.task.location] = server

        if server.status in [Scheduler.ServerDisconnected, Scheduler.ServerAbandoned]:
            if server.rtasks and server.status == Scheduler.ServerDisconnected:
                for _ in range(10):
                    yield task.sleep(0.1)
                    if not server.rtasks:
                        break
        else:
            if (server.status == Scheduler.ServerInitialized or
                server.status == Scheduler.ServerSuspended):
                server.status = Scheduler.ServerClosed
                if not server.cpu_avail.is_set():
                    logger.debug('Waiting for remote tasks at %s to finish', server.task.location)
                    yield server.cpu_avail.wait()
                if await_async:
                    while server.rtasks:
                        rtask, job = server.rtasks[next(iter(server.rtasks))]
                        logger.debug('Remote task %s has not finished yet', rtask)
                        if job.done:
                            yield job.done.wait()
            if server.task:
                server.task.send({'req': 'close', 'auth': computation._auth, 'client': task})
                yield task.receive(timeout=MsgTimeout)
            if server.rtasks:  # wait a bit for server to terminate tasks
                for _ in range(10):
                    yield task.sleep(0.1)
                    if not server.rtasks:
                        break
            server.status = Scheduler.ServerClosed

        if server.rtasks:
            logger.warning('%s tasks abandoned at %s', len(server.rtasks), server.task.location)
            for rtask, job in server.rtasks.values():
                if job.request.endswith('async'):
                    if job.done:
                        job.done.set()
                else:
                    job.client.send(None)
                if status_task:
                    status = pycos.MonitorException(rtask, (Scheduler.TaskAbandoned, None))
                    status_task.send(status)
            server.rtasks.clear()

        if ((server.status == Scheduler.ServerAbandoned and node.abandon_zombie) or
            (server.status != Scheduler.ServerAbandoned)):
            server_task, server.task = server.task, None
            if not server_task:
                raise StopIteration(0)
            node.disabled_servers.pop(server_task.location, None)
            if ((server.status == Scheduler.ServerDisconnected) or
                (server.status == Scheduler.ServerAbandoned and node.abandon_zombie)):
                # TODO: it is not safe to throw away peer if server is still running
                Task(pycos.Pycos.instance().close_peer, server_task.location, timeout=2)
            server.xfer_files = []
            server.askew_results.clear()
            if status_task:
                status_task.send(DispycosStatus(server.status, server_task.location))

        if not server.cpu_avail.is_set():
            server.cpu_avail.set()
            node.cpus_used -= 1
            if node.cpus_used == len(node.servers):
                self._cpu_nodes.discard(node)
                if not self._cpu_nodes:
                    self._cpus_avail.clear()
                node.cpu_avail.clear()
            if node.servers:
                node.load = float(node.cpus_used) / len(node.servers)
            else:
                node.load = 0.0

        if self.__server_locations:
            self.__server_locations.discard(server_task.location)
            # TODO: inform other servers

        raise StopIteration(0)

    def __close_computation(self, client=None, await_async=False, task=None):
        self.__server_locations.clear()
        if self._cur_computation:
            close_tasks = [SysTask(self.__close_node, node, await_async=await_async)
                           for node in self._nodes.values()]
            close_tasks.extend([SysTask(self.__close_node, node)
                                for node in self._disabled_nodes.values()])
            for close_task in close_tasks:
                yield close_task.finish()
        if self.__cur_client_auth:
            computation_path = os.path.join(self.__dest_path, self.__cur_client_auth)
            if os.path.isdir(computation_path):
                shutil.rmtree(computation_path, ignore_errors=True)
        if self._cur_computation and self._cur_computation.status_task:
            self._cur_computation.status_task.send(DispycosStatus(Scheduler.ComputationClosed,
                                                                  id(self._cur_computation)))
        self.__cur_client_auth = self._cur_computation = None
        self.__computation_sched_event.set()
        if client:
            client.send('closed')
        raise StopIteration(0)

    def close(self, task=None):
        """Close current computation and quit scheduler.

        Must be called with 'yield' as 'yield scheduler.close()' or as
        task.
        """
        yield self.__close_computation(task=task)
        raise StopIteration(0)


if __name__ == '__main__':
    """The scheduler can be started either within a client program (if no other
    client programs use the nodes simultaneously), or can be run on a node with
    the options described below (usually no options are necessary, so the
    scheduler can be strated with just 'dispycos.py')
    """

    import logging
    import argparse
    import signal
    try:
        import readline
    except ImportError:
        pass

    import pycos.dispycos
    setattr(sys.modules['pycos.dispycos'], '_DispycosJob_', _DispycosJob_)

    pycos.config.DispycosSchedulerPort = eval(pycos.config.DispycosSchedulerPort)
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip_addr', dest='node', action='append', default=[],
                        help='IP address or host name of this node')
    parser.add_argument('--ext_ip_addr', dest='ext_ip_addr', action='append', default=[],
                        help='External IP address to use (needed in case of NAT firewall/gateway)')
    parser.add_argument('--scheduler_port', dest='scheduler_port', type=str,
                        default=str(pycos.config.DispycosSchedulerPort),
                        help='port number for dispycos scheduler')
    parser.add_argument('--node_port', dest='node_port', type=str,
                        default=str(eval(pycos.config.DispycosNodePort)),
                        help='port number for dispycos node')
    parser.add_argument('--ipv4_udp_multicast', dest='ipv4_udp_multicast', action='store_true',
                        default=False, help='use multicast for IPv4 UDP instead of broadcast')
    parser.add_argument('-n', '--name', dest='name', default=None,
                        help='(symbolic) name given to schduler')
    parser.add_argument('--dest_path', dest='dest_path', default=None,
                        help='path prefix to where files sent by peers are stored')
    parser.add_argument('--max_file_size', dest='max_file_size', default=None, type=int,
                        help='maximum file size of any file transferred')
    parser.add_argument('-s', '--secret', dest='secret', default='',
                        help='authentication secret for handshake with peers')
    parser.add_argument('--certfile', dest='certfile', default='',
                        help='file containing SSL certificate')
    parser.add_argument('--keyfile', dest='keyfile', default='',
                        help='file containing SSL key')
    parser.add_argument('--node', action='append', dest='nodes', default=[],
                        help='additional remote nodes (names or IP address) to use')
    parser.add_argument('--relay_nodes', action='store_true', dest='relay_nodes', default=False,
                        help='request each node to relay scheduler info on its network')
    parser.add_argument('--pulse_interval', dest='pulse_interval', type=float,
                        default=MaxPulseInterval,
                        help='interval in seconds to send "pulse" messages to check nodes '
                        'and client are connected')
    parser.add_argument('--ping_interval', dest='ping_interval', type=float, default=0,
                        help='interval in seconds to broadcast "ping" message to discover nodes')
    parser.add_argument('--zombie_period', dest='zombie_period', type=int,
                        default=(100 * MaxPulseInterval),
                        help='maximum time in seconds computation is idle')
    parser.add_argument('-d', '--debug', action='store_true', dest='loglevel', default=False,
                        help='if given, debug messages are printed')
    parser.add_argument('--clean', action='store_true', dest='clean', default=False,
                        help='if given, files copied from or generated by clients will be removed')
    parser.add_argument('--daemon', action='store_true', dest='daemon', default=False,
                        help='if given, input is not read from terminal')
    config = vars(parser.parse_args(sys.argv[1:]))
    del parser

    if config['zombie_period'] and config['zombie_period'] < MaxPulseInterval:
        raise Exception('zombie_period must be >= %s' % MaxPulseInterval)

    if not config['name']:
        config['name'] = 'dispycos_scheduler'

    if config['loglevel']:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    del config['loglevel']

    if config['certfile']:
        config['certfile'] = os.path.abspath(config['certfile'])
    else:
        config['certfile'] = None
    if config['keyfile']:
        config['keyfile'] = os.path.abspath(config['keyfile'])
    else:
        config['keyfile'] = None

    pycos.config.DispycosSchedulerPort = config.pop('scheduler_port')
    pycos.config.DispycosNodePort = config.pop('node_port')
    daemon = config.pop('daemon', False)

    _dispycos_scheduler = Scheduler(**config)
    _dispycos_scheduler._remote = True
    del config

    def sighandler(signum, frame):
        # Task(_dispycos_scheduler.close).value()
        raise KeyboardInterrupt

    try:
        signal.signal(signal.SIGHUP, sighandler)
        signal.signal(signal.SIGQUIT, sighandler)
    except Exception:
        pass
    signal.signal(signal.SIGINT, sighandler)
    signal.signal(signal.SIGABRT, sighandler)
    signal.signal(signal.SIGTERM, sighandler)
    del sighandler

    if not daemon:
        try:
            if os.getpgrp() != os.tcgetpgrp(sys.stdin.fileno()):
                daemon = True
        except Exception:
            pass

    if daemon:
        del daemon
        while 1:
            try:
                time.sleep(3600)
            except (Exception, KeyboardInterrupt):
                break
    else:
        del daemon
        while 1:
            try:
                _dispycos_cmd = input(
                    '\n\nEnter "quit" or "exit" to terminate dispycos scheduler\n'
                    '      "status" to show status of scheduler: '
                    )
            except KeyboardInterrupt:
                break
            except EOFError:
                logger.warning('EOF ignored!\n')
                continue
            _dispycos_cmd = _dispycos_cmd.strip().lower()
            if _dispycos_cmd in ('quit', 'exit'):
                break
            if _dispycos_cmd == 'status':
                _dispycos_scheduler.print_status()

    logger.info('terminating dispycos scheduler')
    try:
        Task(_dispycos_scheduler.close).value()
    except KeyboardInterrupt:
        pass
