#coding=utf-8
import tensorflow as tf
import numpy as np
import scipy.misc
from io import BytesIO

class Logger(object):
    def __init__(self,log_dir):
        self.writer=tf.summary.FileWriter(log_dir)


    def scalar_summary(self,tag,value,step):
        summary=tf.Summary(value=[tf.Summary.Value(tag=tag,simple_value=value)])
        self.writer.add_summary(summary,step)

    def image_summary(self,tag,images,step):
        img_summaries=[]
        for i,img in enumerate(images):
            s=BytesIO()
        
            scipy.misc.toimage(img).save(s,format='png')
            img_sum=tf.Summary.Image(encoded_image_string=s.getvalue(),height=img.shape[0],width=img.shape[1])

	    # img_sum = tf.Summary.Image(encoded_image_string=s.getvalue(),height=img.shape[0],width=img.shape[1])
            # Create a Summary value
            img_summaries.append(tf.Summary.Value(tag='%s/%d' % (tag, i), image=img_sum))

        # Create and write Summary
        summary = tf.Summary(value=img_summaries)
        self.writer.add_summary(summary, step)

