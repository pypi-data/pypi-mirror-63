..
  Copyright 2017-2019 The FIAAS Authors

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

=============
FIAAS Logging
=============

|Build Badge| |Code quality badge|

.. |Build Badge| image:: https://fiaas-svc.semaphoreci.com/badges/logging.svg?style=shields
    :target: https://fiaas-svc.semaphoreci.com/projects/logging

.. |Code quality badge| image:: https://api.codacy.com/project/badge/Grade/735fe699137c4c1d94748d5c2525157f
   :alt: Codacy Badge
   :target: https://app.codacy.com/gh/fiaas/logging


This library configures logging according to the current FIAAS recomended format.

Usage::

    from fiaas_logging import init_logging

    init_logging(format="json")


This would configure your application to emit JSON formatted logs on STDOUT.

Available options (all are keyword arguments to `init_logging`):


====== =============== =================================================
Key    Possible values Meaning
====== =============== =================================================
format `json`/`plain`  Select either JSON logging, or plain text logging
debug  `True`/`False`  Enable debug logging
====== =============== =================================================

The plain format contains the fields timestamp, level name, message, logger name, and thread name.
In the json format, there are more fields, with more detail. The fields in the json output are:

============ =======================================================================
Name         Meaning
============ =======================================================================
@timestamp   Timestamp of message
@version     Version, legacy field to support ELK stack at FINN (to be removed?)
LocationInfo A structure describing the code location that logged this message
message      The actual log message
extras       A structure containing extra fields. Used for thread context
throwable    A formatted stacktrace if the log message is the result of an exception
============ =======================================================================
