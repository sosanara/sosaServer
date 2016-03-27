from picture.views import (PictureList, PictureDetail)
from userInfo.views import (
    UserDetail, StatisticDetail, HistoryViewSet, GraphViewSet
)


user_detail = UserDetail.as_view()

statistic_detail = StatisticDetail.as_view()

picture_list = PictureList.as_view()

picture_detail = PictureDetail.as_view()

history_list = HistoryViewSet.as_view({
    'get': 'list',
})

history_detail = HistoryViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

graph_list = GraphViewSet.as_view({
    'get': 'list',
})

graph_detail = GraphViewSet.as_view({
    'get': 'retrieve',
})
