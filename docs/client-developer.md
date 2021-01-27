[![powered by ImJoy](https://imjoy.io/static/badge/powered-by-imjoy-badge.svg)](https://imjoy.io/)

# Client developer

## Role

TODO

## User management

User-management is handled by [https://auth0.com/](https://auth0.com/)

TODO what exactly can the client developer do here?

### User groups

TODO what are the user groups, what can they do, what can they see?

* admin: super power (ImJoy core developers for the ImJoy server), you can become one if you set up your own server

## Develop annotation plugin

Data inspection/annotation is done with a customizable Kaibu plugin for ImJoy.

### Template plugin

As a template for annotation plugin see [**here**](https://imjoy.io/#/app?w=cloud-annotation&plugin=imjoy-team/imjoy-cloud-annotation:Nuclei-Cloud-Annotator@stable&upgrade=1).

The plugin provides the most commonly required functionality to retrieve samples, annotate them and send the annotations back to the server.
It can be thus used for many standard multi-user annotation. In order to point it to a new annotation task, only two lines have to be changed:

``` javascript
const TASK_ID = 'demo-annotate-nuclei'
const BASE_URL = 'https://api.imjoy.io'
```

### Developing your own plugin

You can further modify the Kaibu plugin and add more functionality, .e.g by adding widgets. For more information, please see the Kaibu documentation [**here**](https://kaibu.org/docs/#/).

The template plugin already provides a dedicated class permitting a simple syntax to interact with the communication server. For a complete list of the API functions of the task management server, please consult the dedicated documentation [**here**](https://ai.pasteur.fr/docs).