# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 15:35:09 2020

@author: Jerry
"""
# https://haptik.ai/tech/putting-text-on-image-using-python/
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def addTextToImg(img, text = 'test', style={}):
    img = img.copy()
    oriImgType = type(img)
    oriImgMax = np.max(img)
    
    if oriImgType == Image.Image:
        pass
    elif oriImgType==np.ndarray:
        img = Image.fromarray(np.uint8(img*255/oriImgMax))
    else:
        raise ValueError('Image type {} is not supported'.format(oriImgType))
        
    draw = ImageDraw.Draw(img)    
    
    font = style.get('font', 'arial.ttf')
    fontsize = style.get('fontsize', 20)    
    textcolor = style.get('textcolor', 'rgb(128,128,128)')
    textlocation = style.get('textlocation', (10,10))    
    
    draw.text(textlocation, text, 
              fill=textcolor, 
              font=ImageFont.truetype(font, size=fontsize))
    
    if oriImgType == Image.Image:
        pass
    elif oriImgType == np.ndarray:
        img = np.array(img)*oriImgMax/255    
    
    return img

def addSegToImg(img, seg, contourOnly=True, color='blue', opcity=1):
    # Img could be [H,W], [H,W,3], [1,H,W,3] or [1,1,H,W,3]
    
    # if img.shape != seg.shape:
        # raise ValueError('The shape of image and segmentation should be the same')
    img = img.copy()
    oriImgDim = np.ndim(img)
    oriImgShape = np.shape(img)
    
    # Transform img to [H,W,3]
    if oriImgDim==2:
        img = np.stack([img]*3, axis=-1)
    elif oriImgDim == 3 and oriImgShape[2] == 3:
        pass
    elif oriImgDim == 4 and (oriImgShape[0],oriImgShape[3]) == (1,3):
        img = np.squeeze(img)
    elif oriImgDim == 5 and (oriImgShape[0],oriImgShape[1],oriImgShape[3]) == (1,1,3):
        img = np.squeeze(img)
    else:
        raise ValueError('Unsupport img with shape {}'.format(oriImgShape))
    
    if contourOnly:
        seg = seg
    
    if type(color) == str:
        if color.lower() == 'blue':
            color = [0,0,1]
        else:
            print('Unsupported color: {}'.format(color))
    elif type(color) in [list, tuple] and len(color) == 3:
        pass
    else:
        raise ValueError('Unsupport color type {}'.format(type(color)))
        
    img[:,:,0][np.nonzero(seg)] = img[:,:,0][np.nonzero(seg)]*(1-opcity) + color[0]*opcity
    img[:,:,1][np.nonzero(seg)] = img[:,:,1][np.nonzero(seg)]*(1-opcity) + color[1]*opcity
    img[:,:,2][np.nonzero(seg)] = img[:,:,2][np.nonzero(seg)]*(1-opcity) + color[2]*opcity
    # img[:,:,1][seg>0] = img[:,:,1]*(1-opcity) + color[1]*opcity
    # img[:,:,2][seg>0] = img[:,:,2]*(1-opcity) + color[2]*opcity
    
    if oriImgDim == 4:
        img = img[np.newaxis, :,:,:]
    elif oriImgDim == 5:
        img = img[np.newaxis, np.newaxis, :,:,:]
        
    return img

def addSegToVol(img, seg, contourOnly=True, color='blue', opcity=1):
    pass

if __name__ == '__main__':
    testAddText = False
    if testAddText:
        imgNP = np.ones((256,256,3))
        img = Image.fromarray(np.uint8(imgNP))
        # img = Image.open('./Sydney-Opera-House-Displayed-Using-Matplotlib.jpg')
        imgAnnotated = addTextToImg(imgNP, 'HELLO')
        # imgAnnotated[0,0]=0
        
        import matplotlib.pyplot as plt
        plt.imshow(imgAnnotated, cmap='gray')
        
    testAddSegToImg = False
    if testAddSegToImg:
        #img = np.stack([0*np.ones((28,28)),0.5*np.ones((28,28)),0.5*np.ones((28,28))], axis=-1)
        img = np.random.rand(28,28,3)
        seg = np.zeros((28,28));  seg[10:20,10:20] = 1
        imgWithSeg = addSegToImg(img, seg)
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1,2)
        axes[0].imshow(img, cmap='gray')
        axes[1].imshow(imgWithSeg, cmap='gray')
    
    testAll = True
    if testAll:
        shape2D = (256,256)
        img = np.stack([0*np.ones(shape2D),0.5*np.ones(shape2D),0.5*np.ones(shape2D)], axis=-1)
        seg = np.zeros(shape2D);  seg[10:150,10:40] = 1
        imgWithSeg = addSegToImg(img, seg)
        imgWithSegAnnotated = addTextToImg(imgWithSeg, 
                                           text = 'Line 1 \nLine 2',
                                           style={'textcolor':'rgb(255,128,128)'})
        
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1,2)
        axes[0].imshow(img, cmap='gray')
        axes[1].imshow(imgWithSegAnnotated, cmap='gray')