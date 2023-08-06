Assorted debugging facilities.


*Latest release 20200318*:
Remove use of cs.obj.O, universally supplanted by types.SimpleNamespace.

Assorted debugging facilities.

* Lock, RLock, Thread: wrappers for threading facilties; simply import from here instead of there

* thread_dump, stack_dump: dump thread and stack state

* @DEBUG: decorator to wrap functions in timing and value debuggers

* @trace: decorator to report call and return from functions

* @trace_caller: decorator to report caller of function

* TracingObject: subclass of cs.obj.Proxy that reports attribute use

## Function `DEBUG(f, force=False)`

Decorator to wrap functions in timing and value debuggers.

## Function `debug_object_shell(o, prompt=None)`

Interactive prompt for inspecting variables.

## Class `DebuggingLock(DebugWrapper,types.SimpleNamespace)`

Wrapper class for threading.Lock to trace creation and use.
cs.threads.Lock() returns on of these in debug mode or a raw
threading.Lock otherwise.

## Class `DebuggingRLock(DebugWrapper,types.SimpleNamespace)`

Wrapper class for threading.RLock to trace creation and use.
cs.threads.RLock() returns on of these in debug mode or a raw
threading.RLock otherwise.

## Class `DebugShell(cmd.Cmd)`

An interactive prompt for python statements, attached to /dev/tty by default.

## Class `DebugWrapper(types.SimpleNamespace)`

Base class for classes presenting debugging wrappers.

## Function `DF(func, *a, **kw)`

Wrapper for a function call to debug its use.
Requires rewriting the call from f(*a, *kw) to DF(f, *a, **kw).
Alternatively one could rewrite as DEBUG(f)(*a, **kw).

## Function `Lock()`

Factory function: if cs.logutils.logging_level <= logging.DEBUG
then return a DebuggingLock, otherwise a threading.Lock.

## Function `openfiles(substr=None, pid=None)`

Run lsof(8) against process `pid` returning paths of open files whose paths contain `substr`.
`substr`: default substring to select by; default returns all paths.
`pid`: process to examine; default from os.getpid().

## Function `RLock()`

Factory function: if cs.logutils.logging_level <= logging.DEBUG
then return a DebuggingRLock, otherwise a threading.RLock.

## Function `selftest(module_name, defaultTest=None, argv=None)`

Called by my unit tests.

## Function `stack_dump(stack=None, limit=None, logger=None, log_level=None)`

Dump a stack trace to a logger.
`stack`: a stack list as returned by traceback.extract_stack.
         If missing or None, use the result of traceback.extract_stack().
`limit`: a limit to the number of stack entries to dump.
         If missing or None, dump all entries.
`logger`: a logger.Logger ducktype or the name of a logger.
         If missing or None, obtain a logger from logging.getLogger().
`log_level`: the logging level for the dump.
         If missing or None, use cs.logutils.logging_level.

## Function `thread_dump(Ts=None, fp=None)`

Write thread identifiers and stack traces to the file `fp`.
`Ts`: the Threads to dump; if unspecified use threading.enumerate().
`fp`: the file to which to write; if unspecified use sys.stderr.

## Class `TimingOutLock`

A Lock replacement which times out, used for locating deadlock points.

## Function `trace(func)`

Decorator to report the call and return of a function.

## Function `trace_caller(func)`

Decorator to report the caller of a function when called.

## Class `TraceSuite`

Context manager to trace start and end of a code suite.



# Release Log

*Release 20200318*:
Remove use of cs.obj.O, universally supplanted by types.SimpleNamespace.

*Release 20181231*:
New TimingOutLock for locating deadlock points, grew from debugging cs.vt.index.
Other minor changes.

*Release 20171231*:
Update imports for recentchanges.
New context manager TraceSuite to trace start and end of a code suite.

*Release 20160918*:
selftest(): fix parameter ordering to match unittest.

*Release 20160828*:
Update metadata with "install_requires" instead of "requires".

*Release 20160827*:
New openfiles() to return selected pathnames of open files via lsof(8).
New selftest() to invoke unittests with benefits.
DebugShell, a cmd.Cmd subclass for debugging - current use case calls this with self.__dict__ in a test case tearDwon.
debug_object_shell: convenience wrapper for DebugShell to call it on an object's attributes.

*Release 20150116*:
PyPI prep.
