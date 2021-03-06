import caffe
import numpy as np

caffe_root = '../../'

net = caffe.Net(caffe_root + 'models/bvlc_googlenet/deploy.prototxt', 
		caffe_root + 'models/bvlc_googlenet/bvlc_googlenet.caffemodel', 
		caffe.TEST)

cub_net = caffe.Net(caffe_root + 'models/CUB_googLeNet_ST/deploy2.prototxt', 
                    caffe_root + 'models/CUB_googLeNet_ST/caffemodels/CUB_googLeNet_ST_NO_ST_USED_WITH_WEIGHT_DECAY_iter_1000.caffemodel', 
		    caffe.TEST)

net_params = net.params.keys()
prefix_list = ['st']

print net.params.keys()
print cub_net.params.keys()

for param in net_params[:-1]:
    for idx, value in enumerate(net.params[param]):
        for prefix in prefix_list:
            print 'Copying to %s, %d' % ('/'.join([prefix, param]), idx)
            cub_net.params['/'.join([prefix, param])][idx].reshape(*value.data.shape)
            cub_net.params['/'.join([prefix, param])][idx].data[...] = value.data
            
print 'Saving to protobuf file'
cub_net.save(caffe_root + 'models/CUB_googLeNet_ST/init_CUB_googLeNet_ST_NO_ST_USED_WITH_WEIGHT_DECAY.caffemodel')
