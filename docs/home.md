[![powered by ImJoy](https://imjoy.io/static/badge/powered-by-imjoy-badge.svg)](https://imjoy.io/)

# Cloud annotation in ImJoy

?> ImJoy provides a complete solution to perform **collaborative annotation of imaging data in the cloud**. The actual
annotation tool is browser-based, and requires no local installation. Data is stored on a S3 server, and the annotation tasks are
handled by a dedicated task management server. Only the currently displayed image is dowloaded locally. Such an image is marked as locked, 
and can thus not be annotated by another user. This allows concurrent annotation without risking conflicts. 
This documentation describes the **client-side** of ImJoy's cloud annotation tool. Specifically, we address three distinct groups

* **End users**: how to annotate data
* **Task administrators**: how to create a new task and upload data.
* **Client developer**:  designs news tasks and connects it with a dedicated plugin.

For administrators, who want to **setup your own servers**, we refer to the dedicated  guide that you can find here (TODO).

TODO: add screenshot

## How does it work?

1. Data inspection is done with a customized version of [Kaibu](https://kaibu.org/#/app), which can be provided to the end user as a simple URL. 
2. Data is stored on an S3 server, and only the currently displayed imaged stored locally. New annotations results can be sent back to the server.
3. Communication between Kaibu and the S3 server is achieved by a task scheduling server (“task server”). This server provides a set of API functions allowing to retrieve tasks and samples. Please consult the dedicated repository for how to setup these servers (TODO).

TODO: add schematic