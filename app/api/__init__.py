from app.api.bootstrap import api

from app.api.users import UserList, UserDetail, UserRelationship
from app.api.news import NewsList, NewsDetail, NewsRelationship
from app.api.news_comments import NewsCommentList, NewsCommentDetail, NewsCommentRelationship
from app.api.news_subscriptions import NewsSubscriptionList, NewsSubscriptionDetail, NewsSubscriptionRelationship
from app.api.geokrety import GeokretList, GeokretDetail

api.route(UserList, 'users_list', '/users')
api.route(UserDetail, 'user_details', '/users/<int:id>', '/news/<int:news_id>/author', '/news-comments/<int:newscomment_id>/author')
api.route(UserRelationship, 'user_news', '/users/<int:id>/relationship/news')
api.route(UserRelationship, 'user_news_comments', '/users/<int:id>/relationship/news-comments')

api.route(NewsList, 'news_list', '/news', '/users/<int:author_id>/news')
api.route(NewsDetail, 'news_details', '/news/<int:id>', '/news-comments/<int:newscomment_id>/news')
api.route(NewsRelationship, 'news_comments', '/news/<int:id>/relationship/news-comments')
api.route(NewsRelationship, 'news_author', '/news/<int:id>/relationship/author')

api.route(NewsCommentList, 'news_comments_list', '/news-comments', '/users/<int:author_id>/news-comments', '/news/<int:news_id>/news-comments')
api.route(NewsCommentDetail, 'news_comment_details', '/news-comments/<int:id>')
api.route(NewsCommentRelationship, 'news_comments_author', '/news-comments/<int:id>/relationship/author')
api.route(NewsCommentRelationship, 'news_comments_news', '/news-comments/<int:id>/relationship/news')

api.route(NewsSubscriptionList, 'news_subscriptions_list', '/news-subscriptions', '/users/<int:user_id>/news-subscriptions', '/news/<int:news_id>/news-subscriptions')
api.route(NewsSubscriptionDetail, 'news_subscription_details', '/news-subscriptions/<int:id>')
api.route(NewsSubscriptionRelationship, 'news_subscription_user', '/news-subscriptions/<int:id>/relationship/user')
api.route(NewsSubscriptionRelationship, 'news_subscription_news', '/news-subscriptions/<int:id>/relationship/news')

api.route(GeokretList, 'geokrety_list', '/geokrety')
api.route(GeokretDetail, 'geokret_details', '/geokrety/<int:id>')
