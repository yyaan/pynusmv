# Dependencies
This folder contains all the native dependencies that are not expected to be
installed on the system prior to building pynusmv.

Essentially, it ships the source code of the following two other projects:
  - NuSMV   (2.5.4)  which is licensed to you under LGPLv2.
  - MiniSat (070721) which is licensed to you under MIT license.

In addition to that, it also offers a facility to download ZChaff (2007.3.12)
and make pynusmv be linked against that additional solver. However, because of
a license conflict, the very source code of ZChaff is not provided here.

Should you want to get and build your own copy of these projects and not use
the ones provided here, you are more than welcome to download the source code
of these projects from their respective repositories.
