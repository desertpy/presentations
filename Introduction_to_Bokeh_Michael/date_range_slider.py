from bokeh.models.widgets import RangeSlider, Div
from bokeh.models.callbacks import CustomJS
from datetime import datetime, timedelta

def generate_date_range_slider(days=100):
    end = datetime.utcnow()
    start = (datetime.utcnow() - timedelta(days=days))
    step = timedelta(days=1)
    div = Div(text="<b>Date Range: </b>{} - {}".format(start.strftime("%Y/%m/%d"),
                                                start.strftime("%Y/%m/%d")))

    callback = CustomJS(args=dict(text_input=div), code="""
            var f = cb_obj.range
            var st_dt = new Date(0);
            st_dt.setUTCSeconds(f[0])
            var et_dt = new Date(0);
            et_dt.setUTCSeconds(f[1])
            var start = st_dt.toISOString().slice(0,10).replace(/-/g,"/")
            var end = et_dt.toISOString().slice(0,10).replace(/-/g,"/")
            text_input.text = "<b>Date Range: </b>" + start + " - " + end
        """)

    start_num = start.timestamp()
    end_num = end.timestamp()
    step_num = step.total_seconds()
    range_slider = RangeSlider(start=start_num, end=end_num,
                               range=(start_num, end_num),
                               step=step_num, title=None, callback=callback)

    return div, range_slider
