[![powered by ImJoy](https://imjoy.io/static/badge/powered-by-imjoy-badge.svg)](https://imjoy.io/)

# Cloud annotation in ImJoy

?> ImJoy and its AI server provide a complete solution to perform **collaborative annotation of imaging data in the cloud**.

![kaibu-interface](assets/kaibu-interface.jpg ':size=600')

This documentation describes the **client-side** of ImJoy's cloud annotation tool. Specifically, we address three distinct groups

- **End users**: how to annotate data
- **Task administrators**: how to create a new task and upload data.
- **Client developer**:  designs news tasks and connects it with a dedicated plugin.

For administrators, who want to **setup their own servers**, we refer to the dedicated  guide that you can find here (TODO).

## Main features

- The **annotation tool** is browser-based, and requires no local installation.
- **Data storage** is flexibel and be local or on cloud (S3) servers.
- The **annotation tasks** are handled by our ImJoy AI Server, which allows true multi-user annotation by locking samples that are currently being annotated.

## How does this work?

While it is not important for the end user to know how this works, some of you might still be interested
to get some understanding of what's behind the cloud annotation tool.

![ai-server-schematic](assets/ai-server-schematic.png ':size=400')

1. **Data annotation** is done with a customized ImJoy plugin using [Kaibu](https://kaibu.org/#/app), which can be provided to the end user as a simple URL.
2. Data can be **stored** locally or on remote (S3) server, and only the currently annotated imaged are downloaded locally. New annotations results will be sent back to the storage solution.
3. **Communication** between Kaibu and the storage solution is achieved by our  ImJoy AI Server. This server provides a set of API functions allowing to not only retrieve the samples, but also manages the annotation tasks and monitors their progress. Lastly, it managages multi-user access and thus allows collaborative annotations. If you want to know more, please consult the dedicated repository for how to setup these servers (TODO).
