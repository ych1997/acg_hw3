import cv2
import numpy as np
from scipy.sparse import linalg as linalg
from scipy.sparse import lil_matrix as lil_matrix
OMEGA = 0
DEL_OMEGA = 1
OUTSIDE = 2


def point_location(index, mask):
    if in_omega(index,mask) == False:
        return OUTSIDE
    if edge(index,mask) == True:
        return DEL_OMEGA
    return OMEGA


def in_omega(index, mask):
    return mask[index] == 1

def edge(index, mask):
    if in_omega(index,mask) == False: return False
    for pt in get_surrounding(index):
        if in_omega(pt,mask) == False: return True
    return False

def lapl_at_index(source, index):
    i,j = index
    val = (4 * source[i,j])    \
           - (1 * source[i+1, j]) \
           - (1 * source[i-1, j]) \
           - (1 * source[i, j+1]) \
           - (1 * source[i, j-1])
    return val

def mask_indicies(mask):
    nonzero = np.nonzero(mask)
    return zip(nonzero[0], nonzero[1])

def get_surrounding(index):
    i,j = index
    return [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]

def poisson_sparse_matrix(points):
    N = len(list(points))
    print(N)
    A = lil_matrix((N,N))

    for i,index in enumerate(points):
        A[i,i] = 4
        for x in get_surrounding(index):n
            if x not in points: continue
            j = points.index(x)
            A[i,j] = -1
    return A

def process(source, target, mask):
    indicies=[]
    indicies = list(mask_indicies(mask))
    N = len(list(indicies))
    print("N: "+str(N))
    A = poisson_sparse_matrix(indicies)
    b = np.zeros(N)
    for i,index in enumerate(indicies):
        b[i] = lapl_at_index(source, index)
    x = linalg.cg(A, b)
    composite = np.copy(target).astype(int)
    for i,index in enumerate(indicies):
        composite[index] = x[0][i]
    return composite


def preview(source, target, mask):
    return (target * (1.0 - mask)) + (source * (mask))
source="F16Source.jpg"
target="F16Target.jpg"
mask_dist="F16Mask.jpg"
source_img=cv2.imread(source,cv2.IMREAD_COLOR)
target_img=cv2.imread(target,cv2.IMREAD_COLOR)

mask_img=cv2.imread(mask_dist,cv2.IMREAD_GRAYSCALE)
mask=np.atleast_3d(mask_img).astype(np.float)/255.
mask[mask!=1]=0
mask=mask[:,:,0]
channels=source_img.shape[-1]
result_stack=[process(source_img[:,:,i],target_img[:,:,i],mask) for i in range (channels)]
result = cv2.merge(result_stack)
cv2.imwrite("F16_result.jpg", result)
