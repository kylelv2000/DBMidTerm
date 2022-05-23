from pyecharts.charts import Map, Line, Grid, Timeline, Gauge, Page
from pyecharts import options as opts

def makeLineGraph(infos, time_list):           # [[新增],[死亡],[康复]]
    line = (
        Line()
        .add_xaxis(time_list)
        .add_yaxis("新增",
                   y_axis=infos[0],
                   color='green',
                   label_opts=opts.LabelOpts(is_show=False),
                   is_smooth=True)
        .add_yaxis("死亡",
                   y_axis=infos[1],
                   color='gray',
                   label_opts=opts.LabelOpts(is_show=False),
                   is_smooth=True)
        .add_yaxis("康复",
                   y_axis=infos[2],
                   color='red',
                   label_opts=opts.LabelOpts(is_show=False),
                   is_smooth=True)

        .set_global_opts(
            title_opts=opts.TitleOpts(title="{}至{}疫情情况变化".format(time_list[0], time_list[-1]),
                                      pos_left='center', pos_top='5%'),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
        )
    )
    return line

def makeMapGraph(infos, date):
    c = (
        Map()
        .add("现存病例", infos , "world")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="{}世界各地疫情情况".format(date),pos_left='center', pos_top='5%'),
            visualmap_opts=opts.VisualMapOpts(max_=max([_[1] for _ in infos])),
        )
    )
    return c
