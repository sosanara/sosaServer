from picture.views import (PictureList, PictureDetail)
from userInfo.views import (
    StatisticList, UserDetail, GalleryList, GalleryDetail, HistoryList, HistoryDetail
)


user_detail = UserDetail.as_view()

statistic_list = StatisticList.as_view()

picture_list = PictureList.as_view()

picture_detail = PictureDetail.as_view()

gallery_list = GalleryList.as_view()

gallery_detail = GalleryDetail.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

history_list = HistoryList.as_view()

history_detail = HistoryDetail.as_view()
