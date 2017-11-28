from app.api.bootstrap import api
from app.api.geokrety import GeokretDetail, GeokretList, GeokretRelationship
from app.api.news import NewsDetail, NewsList, NewsRelationship
from app.api.news_comments import (NewsCommentDetail, NewsCommentList,
                                   NewsCommentRelationship)
from app.api.news_subscriptions import (NewsSubscriptionDetail,
                                        NewsSubscriptionList,
                                        NewsSubscriptionRelationship)
from app.api.users import UserDetail, UserList, UserRelationship

api.route(UserList, 'users_list', '/users')
api.route(UserDetail, 'user_details',
          '/users/<int:id>',
          '/news/<int:news_id>/author',
          '/news-comments/<int:newscomment_id>/author',
          '/geokrety/<int:geokret_owned_id>/owner',
          '/geokrety/<int:geokret_held_id>/holder')
api.route(UserRelationship, 'user_news', '/users/<int:id>/relationship/news')
api.route(UserRelationship, 'user_news_comments', '/users/<int:id>/relationship/news-comments')
api.route(UserRelationship, 'user_geokrety_owned', '/users/<int:id>/relationship/geokrety-owned')
api.route(UserRelationship, 'user_geokrety_held', '/users/<int:id>/relationship/geokrety-held')

api.route(NewsList, 'news_list', '/news', '/users/<int:author_id>/news')
api.route(NewsDetail, 'news_details', '/news/<int:id>', '/news-comments/<int:newscomment_id>/news')
api.route(NewsRelationship, 'news_comments', '/news/<int:id>/relationship/news-comments')
api.route(NewsRelationship, 'news_author', '/news/<int:id>/relationship/author')

api.route(NewsCommentList, 'news_comments_list',
          '/news-comments',
          '/users/<int:author_id>/news-comments',
          '/news/<int:news_id>/news-comments')
api.route(NewsCommentDetail, 'news_comment_details', '/news-comments/<int:id>')
api.route(NewsCommentRelationship, 'news_comments_author', '/news-comments/<int:id>/relationship/author')
api.route(NewsCommentRelationship, 'news_comments_news', '/news-comments/<int:id>/relationship/news')

api.route(NewsSubscriptionList, 'news_subscriptions_list', '/news-subscriptions',
          '/users/<int:user_id>/news-subscriptions', '/news/<int:news_id>/news-subscriptions')
api.route(NewsSubscriptionDetail, 'news_subscription_details', '/news-subscriptions/<int:id>')
api.route(NewsSubscriptionRelationship, 'news_subscription_user', '/news-subscriptions/<int:id>/relationship/user')
api.route(NewsSubscriptionRelationship, 'news_subscription_news', '/news-subscriptions/<int:id>/relationship/news')

api.route(GeokretList, 'geokrety_list', '/geokrety',
          '/users/<int:owner_id>/geokrety-owned', '/users/<int:holder_id>/geokrety-held')
api.route(GeokretDetail, 'geokret_details', '/geokrety/<int:id>')
api.route(GeokretRelationship, 'geokret_owner', '/geokrety/<int:id>/relationship/owner')
api.route(GeokretRelationship, 'geokret_holder', '/geokrety/<int:id>/relationship/holder')
