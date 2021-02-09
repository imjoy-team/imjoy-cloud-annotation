[![powered by ImJoy](https://imjoy.io/static/badge/powered-by-imjoy-badge.svg)](https://imjoy.io/)

# Users

For each annotation/inspection task, you will receive a URL pointing to the web tool.

For instance, to annotate the results of a nuclear segmentation, click [**here**](https://imjoy.io/lite?plugin=https://github.com/imjoy-team/imjoy-cloud-annotation/blob/main/imjoy-plugins/ImJoy-Cloud-Annotator.imjoy.html). This will open ImJoy in the browser and annotation tool.

To directly try this annotation plugin in the browser, press the `Run` button below.

<!-- ImJoyPlugin: { "type": "web-worker", "hide_code_block": true} -->
```js
class ImJoyPlugin {
    async setup() {}
    async run(ctx) {
        const imjoy = await api.createWindow({src: "https://imjoy.io/#/app?w=sandbox", name: "ImJoy"})
        const annotator = await imjoy.getPlugin('https://github.com/imjoy-team/imjoy-cloud-annotation/blob/main/imjoy-plugins/ImJoy-Cloud-Annotator.imjoy.html')
        await annotator.run()
    }
}
api.export(new ImJoyPlugin())
```

## Open the annotation tool

1. When opening the annotation tool, you will see the basic interface with no data being shown.
2. You then have to click on `Login`. Here, you can either create a new account or use login via an existing account elsewhere (Google account). If the login fails, please provide the email address that you used to the administrator such that you can be added to the white list of people allowed to access the task.
3. Once you login, you will be presented with a pull-down menu where you can see all tasks that are available for your account. As an example, to annotate results of a nuclei segmentation demo select `demo-annotate-nuclei`.

## Display a sample

1. Click on `Get Sample`, this will randomly select a sample that has not been annotated/inspected yet. If another user is annotating the same data, samples will be locked, to avoid that the same sample is annotated at the same time.
2. The sample will then be loaded and the different layers, such as images and annotations, displayed(‘vector’ and ‘dapi.png’ in the example above).
    1. You can toggle the display of a layer by clicking on the eye symbol next to its name.
    2. By clicking on the name of the layer a layer-specific context menu will be displayed (more details below). For instance, for images, you can change the contrast, and for vector layers, you can select objects and delete them, or draw new ones)

## Annotate, save and submit a sample

1. Once a sample is open, you can select the annotation layer (‘vector’ in the example above). You can then:
    * **Delete** an object: choose the ‘Select’ tool, click on the object (it will change color), and press Delete.
    * **Annotate** an object: choose the `Draw` tool and outline the object.
2. Once you are done with the annotation of an image, you can
    * **Save**: which will submit your changes to the server, but NOT mark the sample as complete. You (or somebody else) can later continue working on this sample.
    * **Submit**: submit changes to the server, which will mark the sample being completed.

?> __Note:__ if you are interested in the status of the annotation, e.g. how many samples are completed, press on `Status`.

## Layer-specific context menu

### Images

The context menu for images allows to select channels, change their contrast settings and opacity.

![kaibu-image-menu.png](assets/kaibu-image-menu.png ':size=400')

### Vector layer (for annotation)
The context menu for the vector layer allows to select objects (with the select tool) or to draw new ones with the Draw tool.

![kaibu-vector-menu.png](assets/kaibu-vector-menu.png ':size=400')