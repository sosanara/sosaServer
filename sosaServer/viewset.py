from picture.views import (PictureList, PictureDetail)
from userInfo.views import (
    UserDetail, StatisticDetail, HistoryList, HistoryDetail, GraphList, GraphDetail
)


user_detail = UserDetail.as_view()

statistic_detail = StatisticDetail.as_view()

picture_list = PictureList.as_view()

picture_detail = PictureDetail.as_view()

history_list = HistoryList.as_view()

history_detail = HistoryDetail.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

graph_list = GraphList.as_view()

graph_detail = GraphDetail.as_view()
