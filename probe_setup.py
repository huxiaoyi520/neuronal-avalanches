# 创建模块文件 probe_setup.py：
##步骤如下
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('Qt5Agg')
from probeinterface import Probe
from probeinterface.plotting import plot_probe
from probeinterface import generate_multi_columns_probe

def create_square_probe():

    positions = np.array([[0,0,0],[0,200,0],[0,400,0],[0,600,0],
                      [200,0,0],[200,200,0],[200,400,0],[200,600,0],
                      [400,0,0],[400,200,0],[400,400,0],[400,600,0],
                      [600,0,0],[600,200,0],[600,400,0],[600,600,0]])

    square_probe = generate_multi_columns_probe(num_columns=4,
                                            num_contact_per_column=4,
                                            xpitch=200, ypitch=200,
                                            contact_shapes='circle',
                                            contact_shape_params={'radius': 12.5})
    square_probe.create_auto_shape('rect')
    #plot_probe(square_probe)

    # plt.show()

    # print(square_probe)

    # contact_ids = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'] ###等同下一句代码
    contact_ids = [str(i) for i in range(1, 17)]


    square_probe.set_contact_ids(contact_ids)
    device_channel_indices= np.array([2,6,10,14,15,11,7,3,4,8,12,16,13,9,5,1])-1###这个地方一定是要从0开始计数
    square_probe.device_channel_indices = device_channel_indices
    return square_probe


    # df = square_probe.to_dataframe()
    # df
    # plot_probe(square_probe)
    # probe_3d = square_probe.to_3d(axes='xy')
    # plot_probe(probe_3d)
    # plot_probe(square_probe, with_contact_id=True, with_device_index=True)
if __name__ == "__main__":
    square_probe = create_square_probe()
    # 在这里添加测试代码，例如绘图
    from probeinterface.plotting import plot_probe
    import matplotlib.pyplot as plt

    plot_probe(square_probe, with_contact_id=True, with_device_index=True)
    plt.show()