
import numpy as np
from geojson import Polygon as geojson_polygon
from shapely.geometry import Polygon as shapely_polygon
from geojson import Feature, FeatureCollection
from skimage import measure
from skimage.draw import  polygon

def label_to_geojson(img_label, label, simplify_tol=1.5):
    """
    Function reading a label image, and returning a feature collection
    following the geojson standard. 
    
    Args:
      img_label (numpy array): numpy data, with each object being assigned with a unique uint number
      label (str): like 'cell', 'nuclei'
      simplify_tol (float): give a higher number if you want less coordinates.
    """
    # for img_label, for cells on border, make sure on border pixels are # set to 0
    shape_x, shape_y = img_label.shape
    shape_x, shape_y = shape_x - 1, shape_y - 1
    img_label[0, :] = img_label[:, 0] = img_label[shape_x, :] = img_label[:, shape_y] = 0
    features = []
    
    # Get all object ids, remove 0 since this is background
    ind_objs = np.unique(img_label)
    ind_objs = np.delete(ind_objs, np.where(ind_objs == 0))
    
    for obj_int in np.nditer(ind_objs, flags=["zerosize_ok"]):
        
        # Create binary label for current object and find contour
        img_label_loop = np.zeros((img_label.shape[0], img_label.shape[1]))
        img_label_loop[img_label == obj_int] = 1
        contours_find = measure.find_contours(img_label_loop, 0.5)
       
        if len(contours_find) == 1:
            index = 0
        else:
            pixels = []
            for _, item in enumerate(contours_find):
                pixels.append(len(item))
            index = np.argmax(pixels)
        contour = contours_find[index]

        contour_as_numpy = contour[:, np.argsort([1, 0])].astype('uint16')
        contour_as_numpy[:, 1] = np.array([img_label.shape[0] - h[0] for h in contour])
        contour_asList = contour_as_numpy.tolist()

        if simplify_tol is not None:
            poly_shapely = shapely_polygon(contour_asList)
            poly_shapely_simple = poly_shapely.simplify(
                simplify_tol, preserve_topology=False
            )
            contour_asList = list(poly_shapely_simple.exterior.coords)

        # Create and append feature for geojson
        pol_loop = geojson_polygon([contour_asList])

        full_label = label + "_idx"
        index_number = int(obj_int - 1)
        features.append(
            Feature(
                geometry=pol_loop, properties={full_label: index_number, "label": label}
            )
        )

    feature_collection = FeatureCollection(features, bbox=[0, 0, img_label.shape[1]-1, img_label.shape[0]-1])
    
    return feature_collection, features

def geojson_to_label(data_json, img_size, binary_labeling=False):
    """
    Function reading a geojson and returning a label image array

    Args:
      data_json (dict): dictionary in the geojson format containing coordionate of object to label
      img_size (tuple int): size of the original labelled image
      binary_labeling (bool): if True it does not separate connected componnent and use 1 as label for all polygon
      if False the N objects are number 1,2,3,...N
    """

    def make_mask(roi_pos, img_size):
        rr, cc = polygon(roi_pos[:, 0], roi_pos[:, 1])
        # Make sure it's not outside
        rr[rr < 0] = 0
        rr[rr > img_size[0] - 1] = img_size[0] - 1
        cc[cc < 0] = 0
        cc[cc > img_size[1] - 1] = img_size[1] - 1
        # Generate mask
        mask = np.zeros(img_size, dtype=np.uint8)
        mask[rr, cc] = 1
        return mask

    mask_loop = np.zeros(img_size)
    for i in range(len(data_json['features'])):
        try:
            reg_pos = np.squeeze(np.asarray(data_json['features'][i]['geometry']['coordinates']))
        except KeyError:
            pass  # GeometryCollection
        if len(reg_pos.shape) == 1:  # case where the label is a point
            reg_pos = np.array([reg_pos])
        reg_pos[:, [0, 1]] = reg_pos[:, [1, 0]]  # inverse coordinate from kaibu
        reg_pos[:, 0] = -1*reg_pos[:, 0]+img_size[0]
        if binary_labeling:
            mask_loop += make_mask(reg_pos, img_size)
        else:
            mask_loop += make_mask(reg_pos, img_size) * (i+1)  # N objectS are number 1,2,3,...N
    return mask_loop
