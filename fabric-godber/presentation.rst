Task Automation with Fabric
===========================

Austin Godber

godber@uberhip.com

@godber

4/24/2013

----

Fabric - Intro
==============

Fabric is a Python library that simplifies system automation tasks, both local and remote.

* Python and Shell Task Execution
* Local Tasks
* Remote Tasks
* Privileged execution with sudo
* Get/put files
* User prompts
* Great docs at: http://docs.fabfile.org/

----

Obligatory Hello World
======================

To get started

* instal fabric in a virtualenv via: ``pip install fabic``
* start a ``fabfile.py`` with your favorite editor and add the following
  example

.. sourcecode:: python

   def greet():
     print('Hello World')

* Check available tasks with: ``fab -l``::

    Available commands:

        greet

* Run task with ``fab greet``::

    Hello World

    Done.

----

Improvement 1 - Task Descriptions
=================================

You can provide task descriptions by supplying a docstring in your function definition

.. sourcecode:: python

   def greet():
     """Greet everyone"""
     print('Hello World')

Thus, `fab -l` results in::

  Available commands:

      greet  Greet Everyone

Instead of just::

  Available commands:

      greet


----

Improvement 2 - Task Arguments
==============================

You can provide arguments to tasks as well

.. sourcecode:: python

   def greet(name='World'):
     """Greet everyone"""
     print('Hello %s')

Calling with an argument, like: `fab greet:Skrillex` results in::

   Hello Skrillex

   Done.

----

So what? Thats just Python.
============================

----

This isn't.
===========

----

Deploying Flask - Part 1
========================

I can package and deploy my Flask website with the command: `fab prod deploy`
or `fab stage deploy`.

.. sourcecode:: python

  from fabric.api import run, local, env, get
  from fabric.context_managers import cd
  from fabric.operations import put, sudo
  from fabric.contrib.files import exists
  import time

  def prod():
      '''Configuration for Production Environment'''
      env.db = 'desertpy_prod'
      env.hosts = ['godber@webhost.desertpy.com']

  def stage():
      '''Configuration for Staging Environment'''
      env.db = 'desertpy_dev'
      env.hosts = ['godber@webstage.desertpy.com']

  # continued ...

----

Deploying Flask - Part 1
========================

.. sourcecode:: python

  # ... continuation
  def deploy():
      '''Deploys a tar file from the latest hg revision'''
      hg_version = local('hg identify -i', capture=True).strip()
      timestamp = time.time()
      prefix = "myapp-%s-%s" % (timestamp, hg_version)
      filename = 'myapp-%s-%s.tgz' % (timestamp, hg_version)
      filepath = '/tmp/%s' % filename
      local('hg archive -p %s %s' % (prefix, filepath))
      with cd('/var/app'):
          put(filepath, "src")
          run('tar -zxf src/%s' % filename)
          run('rm myapp-last')
          run('mv myapp myapp-last')
          run('ln -fs %s myapp' % prefix )
          if exists('myapp-cfg/local_cfg.py'):
              run('cp myapp-cfg/local_cfg.py myapp/myapp/local_cfg.py')
          sudo('supervisorctl restart myapp')
      local('rm %s' % filepath)

----

Breaking it Down - Setup
========================

Configuration via tasks and the `env` global dictionary.

.. sourcecode:: python

  from fabric.api import env

I set some variables I want accessible by all tasks.

.. sourcecode:: python

  def prod():
      '''Configuration for Production Environment'''
      env.db = 'desertpy_prod'
      env.hosts = ['godber@webhost.desertpy.com']

  def stage():
      '''Configuration for Staging Environment'''
      env.db = 'desertpy_dev'
      env.hosts = ['godber@webstage.desertpy.com']

  #...

Hosts can also be specified as an argument to the fab command itself, with the
`-H` option.

----

Breaking it down - Packaging
============================

Work on the local machine gets done.

.. sourcecode:: python

  from fabric.api import run, local, env, get

.. sourcecode:: python

  def deploy():
      '''Deploys a tar file from the latest hg revision'''
      hg_version = local('hg identify -i', capture=True).strip()
      timestamp = time.time()
      prefix = "myapp-%s-%s" % (timestamp, hg_version)
      filename = 'myapp-%s-%s.tgz' % (timestamp, hg_version)
      filepath = '/tmp/%s' % filename
      local('hg archive -p %s %s' % (prefix, filepath))
      #...


----

In Essence
==========

Run local or remote commands on one or more computers, via ssh as root or not.

.. sourcecode:: python

  from fabric.api import run
  from fabric.decorators import hosts

  @hosts('monk','zag.local','europa.local')
  def name():
      """Print out the hostname and system information"""
      run('hostname')
      run('uname -a')

----

In Essence - Output
===================

Run `fab name`::

  [monk] Executing task 'name'
  [monk] run: hostname
  [monk] out: monk
  [monk] out: 

  [monk] run: uname -a
  [monk] out: Linux monk 3.2.0-40-generic #64-Ubuntu SMP Mon Mar 25 21:22:10 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux
  [monk] out: 

  [zag.local] Executing task 'name'
  [zag.local] run: hostname
  [zag.local] out: zag.local
  [zag.local] out: 

  [zag.local] run: uname -a
  [zag.local] out: Darwin zag.local 12.3.0 Darwin Kernel Version 12.3.0: Sun Jan  6 22:37:10 PST 2013; root:xnu-2050.22.13~1/RELEASE_X86_64 x86_64
  [zag.local] out: 

  [europa.local] Executing task 'name'
  [europa.local] run: hostname
  [europa.local] out: europa.local
  [europa.local] out: 

  [europa.local] run: uname -a
  [europa.local] out: Darwin europa.local 11.4.2 Darwin Kernel Version 11.4.2: Thu Aug 23 16:25:48 PDT 2012; root:xnu-1699.32.7~1/RELEASE_X86_64 x86_64
  [europa.local] out: 


  Done.
  Disconnecting from zag.local... done.
  Disconnecting from monk... done.
  Disconnecting from europa.local... done.

----
