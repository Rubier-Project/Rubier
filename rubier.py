import rubier.httpz as httpz
import rubier.randomStream as randomStream
import rubier.copyrights as copyrights
import rubier.servers as servers
import requests
import pathlib
import json
import io
import base64
import PIL.Image
import aiohttp
import threading
import asyncio

# Available the copyrights
copyrights.ConsoleCopyrights.consolePrinter()

# Main Class
class Rubier(object):
    def __init__(self, AuthToken: str):
        self.auth = AuthToken

    def makeInsideRequestsClass(self, inData,method):
        data = {
                "api_version": "0",
                "auth": self.auth,
                "client": {
                    "app_name": "Main",
                    "app_version": "3.0.2",
                    "lang_code": "fa",
                    "package": "app.rbmain.a",
                    "platform": "Android"
                    },
                "data": inData,
                "method": method
                }
        while True:
            try:
                return requests.post(servers.RubinoApi.getApi(), json=data).json()
            except:
                continue

    def requestUploadFile(self,file,size=None, Type="Picture",prof=None):
        inData = {
			"file_name": file.split("/")[-1],
			"file_size": size or pathlib.Path(file).stat().st_size,
			"file_type": Type,
			"profile_id": prof}
        method = "requestUploadFile"
        while True:
            try:
                return self.makeInsideRequestsClass(inData,method)
            except:continue

    @staticmethod
    def _getThumbInline(image_bytes:bytes):
        import io, base64, PIL.Image
        im = PIL.Image.open(io.BytesIO(image_bytes))
        width, height = im.size
        if height > width:
            new_height = 40
            new_width  = round(new_height * width / height)
        else:
            new_width  = 40
            new_height = round(new_width * height / width)
        im = im.resize((new_width, new_height), PIL.Image.ANTIALIAS)
        changed_image = io.BytesIO()
        im.save(changed_image, format='PNG')
        changed_image = changed_image.getvalue()
        return base64.b64encode(changed_image)

    @staticmethod
    def _getImageSize(image_bytes:bytes):
        import io, PIL.Image
        im = PIL.Image.open(io.BytesIO(image_bytes))
        width, height = im.size
        return [width , height]

    def upload(self,file,Type):
        if not "http" in file:
            REQUEST = self.requestUploadFile(file)["data"]
            bytef = open(file,"rb").read()
            file_id = REQUEST["file_id"]
            hash_send = REQUEST["hash_file_request"]
            url = REQUEST["server_url"]
            header = {
        'auth':self.auth,
        'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
        'chunk-size':str(pathlib.Path(file).stat().st_size),
        'file-id':str(file_id),
        'hash-file-request':hash_send,
        "content-type": "application/octet-stream",
        "content-length": str(pathlib.Path(file).stat().st_size),
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.12.1",
        "part-number":"1",
        "total-part":"1"}
            j = requests.post(data=bytef, url=url, headers=header).text
            j = json.loads(j)['data']['hash_file_receive']


            return [REQUEST, j]
        else:
            REQUEST = {
            "file_name": file.split("/")[-1],
            "file_size": pathlib.Path(file).stat().st_size,
            "file_type": Type,
            "profile_id": ""}
            method = "requestUploadFile"
            while True:
                try:
                    return self.makeInsideRequestsClass(REQUEST, method)
                except:continue

    def addPost(self, filePath: str, caption: str = None, isMultiFile=None, postType="Picture", profileID=None):
        fileRespone = Rubier(self.auth).upload(filePath, postType)
        _hash = fileRespone[1]
        fileID = fileRespone[0]["file_id"]
        thumbnailID = fileRespone[0]["file_id"]
        thumbnailHash = fileRespone[1]
        return httpz.Httpz(self.auth).poolConnection({"caption": caption,
                                                      "file_id": fileID,
                                                      "hash_file_receive": _hash,
                                                      "height": 800,
                                                      "width": 800,
                                                      "is_multi_file": isMultiFile,
                                                      "post_type": postType,
                                                      "rnd": randomStream.Stream.randomIntSteram(),
                                                      "thumbnail_file_id": thumbnailID,
                                                      "thumbnail_hash_file_receive": thumbnailHash,
                                                      "profile_id": profileID}
                                                      , "addPost")

    def addPostViewCount(self, postID, postProfileID):
        return httpz.Httpz(self.auth).poolConnection({
            "post_id": postID,
            "post_profile_id": postProfileID
        }, "addPostViewCount")

    def addViewStory(self, storyProfileID, storyIDs: list, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "profile_id": profileID,
            "story_ids": [storyIDs],
            "story_profile_id": storyProfileID
        }, "addViewStory")

    def checkUsernameExists(self, username: str):
        userUsername = False

        if username.startswith("@"):
            userUsername = username.replace("@", "")
        else:userUsername = username

        return httpz.Httpz(self.auth).poolConnection({
            "username": userUsername
        }, "isExistUsername")

    def createPage(self, name: str, username: str, bio: str = None):
        return httpz.Httpz(self.auth).poolConnection({
            "bio": bio,
            "name": name,
            "username": username
        }, "createPage")

    def sendComment(self, text: str, postID, postProfileID, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "content": text,
            "post_id": postID,
            "post_profile_id": postProfileID,
            "rnd":f"{randomStream.Stream.randomIntSteram()}",
            "profile_id": profileID
        }, "addComment")

    def followPage(self, followID, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "f_type": "Follow",
            "followee_id": followID,
            "profile_id": profileID
        }, "requestFollow")

    def unfollowPage(self, followID, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "f_type": "Unfollow",
            "followee_id": followID,
            "profile_id": profileID
        }, "requestFollow")

    def blockPage(self, blockedID, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "action":"Block",
            "blocked_id":blockedID,
            "profile_id":profileID
            }, "setBlockProfile")

    def unBlockPage(self, blockedID, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "action":"Unblock",
            "blocked_id":blockedID,
            "profile_id":profileID
            }, "setBlockProfile")

    def getPostComments(self, postID, postProfileID, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "equal": False,
            "limit": 100,
            "sort": "FromMax",
            "post_id": postID,
            "profile_id": profileID,
            "post_profile_id": postProfileID
        }, "getComments")

    def getMyProfileInfo(self, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "profile_id": profileID
        }, "getMyProfileInfo")

    def getMe(self, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "profile_id": profileID
        }, "getMyProfileInfo")

    def getPostByLink(self, link: str, profileID = None):
        if link.startswith("post/"):
            splitted = link.split("post/")
            inputData = {
                "share_string":splitted,
                "profile_id":profileID
                }
            return httpz.Httpz(self.auth).poolConnection(inputData=inputData, method="getPostByShareLink")
        else:
            inputData = {
                "share_string":link,
                "profile_id":profileID
            }
            return httpz.Httpz(self.auth).poolConnection(inputData=inputData, method="getPostByShareLink")

    def getProfileList(self, limit: int = 10):
        return httpz.Httpz(self.auth).poolConnection({
            "equal": False,
            "limit": limit,
            "sort": "FromMax"
        }, "getProfileList")

    def getProfileStories(self, profileID = None, limit: int = 100):
        return httpz.Httpz(self.auth).poolConnection({
            "limit": limit,
            "profile_id": profileID
        }, "getProfileStories")

    def getRecentFollowingPosts(self, profileID = None, limit: int = 30):
        return httpz.Httpz(self.auth).poolConnection({
            "equal":False,
            "limit": limit,
            "sort":"FromMax",
            "profile_id": profileID
        }, "getRecentFollowingPosts")

    def getShareLink(self, postID, postProfileID, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "post_id":postID,
            "post_profile_id":postProfileID,
            "profile_id":profileID
        }, "getShareLink")

    def getStoryIDs(self, targetProfileID, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "profile_id":profileID,
            "target_profile_id":targetProfileID
        }, "getStoryIds")

    def savePost(self, postID, postProfileID, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "action_type":"Bookmark",
            "post_id":postID,
            "post_profile_id":postProfileID,
            "profile_id":profileID
        }, "postBookmarkAction")

    def updateProfile(self, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "profile_id":profileID,
            "profile_status":"Public"
        }, "updateProfile")

    def likePost(self, postID, postProfileID, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "action_type":"Like",
            "post_id":postID,
            "post_profile_id":postProfileID,
            "profile_id":profileID
        }, "likePostAction")

    def unlikePost(self, postID, postProfileID, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "action_type":"Unlike",
            "post_id":postID,
            "post_profile_id":postProfileID,
            "profile_id":profileID
        }, "likePostAction")

    def likeComment(self, commentID, postID, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "action_type": "Like",
            "comment_id": commentID,
            "post_id": postID,
            "profile_id": profileID
        }, "likeCommentAction")

    def unlikeComment(self, commentID, postID, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "action_type": "Unlike",
            "comment_id": commentID,
            "post_id": postID,
            "profile_id": profileID
        }, "likeCommentAction")

    def getSavePosts(self, limit: int = 10, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "equal":False,
            "limit":limit,"sort":"FromMax",
            "profile_id":profileID
        }, "getBookmarkedPosts")

    def getArchiveStories(self, limit: int = 10, startID = None, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "equal":False,
            "limit":limit,
            "start_id": startID,
            "sort":"FromMax",
            "profile_id":profileID
        }, "getMyArchiveStories")

    def getProfileHighlights(self, targetProfileID, limit: int = 10, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "equal":False,
            "limit":limit,"sort":"FromMax",
            "target_profile_id":targetProfileID,
            "profile_id":profileID
            },"getProfileHighlights")

    def getBlockedProfiles(self, limit: int = 50, maxid = None, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "equal":False,
            "limit":limit,
            "max_id":maxid,
            "sort":"FromMax",
            "profile_id":profileID}, "getBlockedProfiles")

    def getProfileFollowers(self, targetProfileID, limit: int = 50, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "equal":False,
            "f_type":"Following",
            "limit":limit,"sort":"FromMax",
            "target_profile_id":targetProfileID,
            "profile_id":profileID}, "getProfileFollowers")

    def getMyStoriesList(self, limit: int = None, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "limit":limit,
            "profile_id":profileID}, "getMyStoriesList")

    def deleteStory(self, storyID, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "profile_id":profileID,
            "story_id":storyID}, "deleteStory")

    def getExplorePosts(self, topicID, limit: int = 51, maxid = None, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "equal":False,
            "limit":limit,
            "max_id":maxid,
            "sort":"FromMax",
            "topic_id":topicID,
            "profile_id":profileID}, "getExplorePosts")

    def unsavePost(self, postID, postProfileID, profileID = None):
        return httpz.Httpz(self.auth).poolConnection({
            "action_type":"Unbookmark",
            "post_id":postID,
            "post_profile_id":postProfileID,
            "profile_id":profileID
        }, "postBookmarkAction")

    def searchProfile(self, username: str, limit: int = 50, profileID = None):

      userUsername = False

      if username.startswith("@"):
        userUsername = username.replace("@", "")
      else:userUsername = username

      return httpz.Httpz(self.auth).poolConnection({"equal":False,
      "limit":limit,
      "sort":"FromMax",
      "username":userUsername,
      "profile_id":profileID
      }, 'searchProfile')

    def searchinRubino(self, username: str, limit: int = 50, profileID = None):

      userUsername = False

      if username.startswith("@"):
        userUsername = username.replace("@", "")
      else:userUsername = username

      return httpz.Httpz(self.auth).poolConnection({"equal":False,
      "limit":limit,
      "sort":"FromMax",
      "username":userUsername,
      "profile_id":profileID
      }, 'searchProfile')

    def getHashTagTrend(self, limit: int = 50, profileID = None):
      return httpz.Httpz(self.auth).poolConnection({
        "equal":False,
        "limit":limit,
        "sort":"FromMax",
        "profile_id":profileID},"getHashTagTrend")

    def searchHashTag(self, content: str, limit: int = 50, profileID = None):
      return httpz.Httpz(self.auth).poolConnection({
        "content":content,
        "equal":False,"limit":limit,
        "sort":"FromMax",
        "profile_id":profileID }, "searchHashTag")

    def getPostsByHashTag(self, hashtag: str, limit: int = 51, profileID = None):
      return httpz.Httpz(self.auth).poolConnection({
        "equal":False,
        "hashtag": hashtag,
        "limit":limit,
        "profile_id":profileID}, 'getPostsByHashTag')
    
    def getUserInfoByPostLink(self, link: str):
        postLinkInfo = self.getPostByLink(link=link)
        return postLinkInfo['data']['profile'] if "data" in postLinkInfo.keys() else None

class rubino(Rubier):
    ...

class Rubino(Rubier):
    ...

class AsyncRubier(object):
    def __init__(self, AuthToken: str):
        self.auth = AuthToken

    async def makeInsideRequestsClass(self, inData,method):
        data = {
                "api_version": "0",
                "auth": self.auth,
                "client": {
                    "app_name": "Main",
                    "app_version": "3.0.2",
                    "lang_code": "fa",
                    "package": "app.rbmain.a",
                    "platform": "Android"
                    },
                "data": inData,
                "method": method
                }
        while True:
            try:
                async with aiohttp.ClientSession() as sessoin:
                    async with sessoin.post(servers.RubinoApi.getApi(), json=data) as resp:
                        return await resp.json()
            except:
                continue

    async def requestUploadFile(self,file: str,size=None, Type="Picture",prof=None):
        inData = {
			"file_name": file.split("/")[-1],
			"file_size": size or pathlib.Path(file).stat().st_size,
			"file_type": Type,
			"profile_id": prof}
        method = "requestUploadFile"
        while True:
            try:
                return await self.makeInsideRequestsClass(inData,method)
            except:continue

    @staticmethod
    async def _getThumbInline(image_bytes:bytes):
        im = PIL.Image.open(io.BytesIO(image_bytes))
        width, height = im.size
        if height > width:
            new_height = 40
            new_width  = round(new_height * width / height)
        else:
            new_width  = 40
            new_height = round(new_width * height / width)
        im = im.resize((new_width, new_height), PIL.Image.ANTIALIAS)
        changed_image = io.BytesIO()
        im.save(changed_image, format='PNG')
        changed_image = changed_image.getvalue()
        return base64.b64encode(changed_image)

    @staticmethod
    async def _getImageSize(image_bytes:bytes):
        im = PIL.Image.open(io.BytesIO(image_bytes))
        width, height = im.size
        return [width , height]

    async def upload(self,file,Type):
        if not "http" in file:
            REQUEST = self.requestUploadFile(file)["data"]
            bytef = open(file,"rb").read()
            file_id = REQUEST["file_id"]
            hash_send = REQUEST["hash_file_request"]
            url = REQUEST["server_url"]
            header = {
        'auth':self.auth,
        'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
        'chunk-size':str(pathlib.Path(file).stat().st_size),
        'file-id':str(file_id),
        'hash-file-request':hash_send,
        "content-type": "application/octet-stream",
        "content-length": str(pathlib.Path(file).stat().st_size),
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.12.1",
        "part-number":"1",
        "total-part":"1"}
            j = requests.post(data=bytef, url=url, headers=header).text
            j = json.loads(j)['data']['hash_file_receive']


            return [REQUEST, j]
        else:
            REQUEST = {
            "file_name": file.split("/")[-1],
            "file_size": pathlib.Path(file).stat().st_size,
            "file_type": Type,
            "profile_id": ""}
            method = "requestUploadFile"
            while True:
                try:
                    return await self.makeInsideRequestsClass(REQUEST, method)
                except:continue

    async def addPost(self, filePath: str, caption: str = None, isMultiFile=None, postType="Picture", profileID=None):
        fileRespone = Rubier(self.auth).upload(filePath, postType)
        _hash = fileRespone[1]
        fileID = fileRespone[0]["file_id"]
        thumbnailID = fileRespone[0]["file_id"]
        thumbnailHash = fileRespone[1]
        return await httpz.AsyncHttpz(self.auth).poolConnection({"caption": caption,
                                                      "file_id": fileID,
                                                      "hash_file_receive": _hash,
                                                      "height": 800,
                                                      "width": 800,
                                                      "is_multi_file": isMultiFile,
                                                      "post_type": postType,
                                                      "rnd": randomStream.Stream.randomIntSteram(),
                                                      "thumbnail_file_id": thumbnailID,
                                                      "thumbnail_hash_file_receive": thumbnailHash,
                                                      "profile_id": profileID}
                                                      , "addPost")

    async def addPostViewCount(self, postID, postProfileID):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "post_id": postID,
            "post_profile_id": postProfileID
        }, "addPostViewCount")

    async def addViewStory(self, storyProfileID, storyIDs: list, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "profile_id": profileID,
            "story_ids": [storyIDs],
            "story_profile_id": storyProfileID
        }, "addViewStory")

    async def checkUsernameExists(self, username: str):
        userUsername = False

        if username.startswith("@"):
            userUsername = username.replace("@", "")
        else:userUsername = username

        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "username": userUsername
        }, "isExistUsername")

    async def createPage(self, name: str, username: str, bio: str = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "bio": bio,
            "name": name,
            "username": username
        }, "createPage")

    async def sendComment(self, text: str, postID, postProfileID, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "content": text,
            "post_id": postID,
            "post_profile_id": postProfileID,
            "rnd":f"{randomStream.Stream.randomIntSteram()}",
            "profile_id": profileID
        }, "addComment")

    async def followPage(self, followID, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "f_type": "Follow",
            "followee_id": followID,
            "profile_id": profileID
        }, "requestFollow")

    async def unfollowPage(self, followID, profileID = None):
        return httpz.AsyncHttpz(self.auth).poolConnection({
            "f_type": "Unfollow",
            "followee_id": followID,
            "profile_id": profileID
        }, "requestFollow")

    async def blockPage(self, blockedID, profileID = None):
        return httpz.AsyncHttpz(self.auth).poolConnection({
            "action":"Block",
            "blocked_id":blockedID,
            "profile_id":profileID
            }, "setBlockProfile")

    async def unBlockPage(self, blockedID, profileID = None):
        return httpz.AsyncHttpz(self.auth).poolConnection({
            "action":"Unblock",
            "blocked_id":blockedID,
            "profile_id":profileID
            }, "setBlockProfile")

    async def getPostComments(self, postID, postProfileID, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "equal": False,
            "limit": 100,
            "sort": "FromMax",
            "post_id": postID,
            "profile_id": profileID,
            "post_profile_id": postProfileID
        }, "getComments")

    async def getMyProfileInfo(self, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "profile_id": profileID
        }, "getMyProfileInfo")

    async def getMe(self, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "profile_id": profileID
        }, "getMyProfileInfo")

    async def getPostByLink(self, link: str, profileID = None):
        if link.startswith("post/"):
            splitted = link.replace("post/", "")
            inputData = {
                "share_string":splitted,
                "profile_id":profileID
                }
            return await httpz.AsyncHttpz(self.auth).poolConnection(inputData=inputData, method="getPostByShareLink")
        else:
            inputData = {
                "share_string":link,
                "profile_id":profileID
            }
            return await httpz.AsyncHttpz(self.auth).poolConnection(inputData=inputData, method="getPostByShareLink")

    async def getProfileList(self, limit: int = 10):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "equal": False,
            "limit": limit,
            "sort": "FromMax"
        }, "getProfileList")

    async def getProfileStories(self, profileID = None, limit: int = 100):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "limit": limit,
            "profile_id": profileID
        }, "getProfileStories")

    async def getRecentFollowingPosts(self, profileID = None, limit: int = 30):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "equal":False,
            "limit": limit,
            "sort":"FromMax",
            "profile_id": profileID
        }, "getRecentFollowingPosts")

    async def getShareLink(self, postID, postProfileID, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "post_id":postID,
            "post_profile_id":postProfileID,
            "profile_id":profileID
        }, "getShareLink")

    async def getStoryIDs(self, targetProfileID, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "profile_id":profileID,
            "target_profile_id":targetProfileID
        }, "getStoryIds")

    async def savePost(self, postID, postProfileID, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "action_type":"Bookmark",
            "post_id":postID,
            "post_profile_id":postProfileID,
            "profile_id":profileID
        }, "postBookmarkAction")

    async def unsavePost(self, postID, postProfileID, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "action_type":"Unbookmark",
            "post_id":postID,
            "post_profile_id":postProfileID,
            "profile_id":profileID
        }, "postBookmarkAction")

    async def updateProfile(self, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "profile_id":profileID,
            "profile_status":"Public"
        }, "updateProfile")

    async def likePost(self, postID, postProfileID, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "action_type":"Like",
            "post_id":postID,
            "post_profile_id":postProfileID,
            "profile_id":profileID
        }, "likePostAction")

    async def unlikePost(self, postID, postProfileID, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "action_type":"Unlike",
            "post_id":postID,
            "post_profile_id":postProfileID,
            "profile_id":profileID
        }, "likePostAction")

    async def likeComment(self, commentID, postID, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "action_type": "Like",
            "comment_id": commentID,
            "post_id": postID,
            "profile_id": profileID
        }, "likeCommentAction")

    async def unlikeComment(self, commentID, postID, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "action_type": "Unlike",
            "comment_id": commentID,
            "post_id": postID,
            "profile_id": profileID
        }, "likeCommentAction")

    async def getSavePosts(self, limit: int = 10, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "equal":False,
            "limit":limit,"sort":"FromMax",
            "profile_id":profileID
        }, "getBookmarkedPosts")

    async def getArchiveStories(self, limit: int = 10, startID = None, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "equal":False,
            "limit":limit,
            "start_id": startID,
            "sort":"FromMax",
            "profile_id":profileID
        }, "getMyArchiveStories")

    async def getProfileHighlights(self, targetProfileID, limit: int = 10, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "equal":False,
            "limit":limit,"sort":"FromMax",
            "target_profile_id":targetProfileID,
            "profile_id":profileID
            },"getProfileHighlights")

    async def getBlockedProfiles(self, limit: int = 50, maxid = None, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "equal":False,
            "limit":limit,
            "max_id":maxid,
            "sort":"FromMax",
            "profile_id":profileID}, "getBlockedProfiles")

    async def getProfileFollowers(self, targetProfileID, limit: int = 50, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "equal":False,
            "f_type":"Following",
            "limit":limit,"sort":"FromMax",
            "target_profile_id":targetProfileID,
            "profile_id":profileID}, "getProfileFollowers")

    async def getMyStoriesList(self, limit: int = None, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "limit":limit,
            "profile_id":profileID}, "getMyStoriesList")

    async def deleteStory(self, storyID, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "profile_id":profileID,
            "story_id":storyID}, "deleteStory")

    async def getExplorePosts(self, topicID, limit: int = 51, maxid = None, profileID = None):
        return await httpz.AsyncHttpz(self.auth).poolConnection({
            "equal":False,
            "limit":limit,
            "max_id":maxid,
            "sort":"FromMax",
            "topic_id":topicID,
            "profile_id":profileID}, "getExplorePosts")

    async def searchProfile(self, username: str, limit: int = 50, profileID = None):

      userUsername = False

      if username.startswith("@"):
        userUsername = username.replace("@", "")
      else:userUsername = username

      return await httpz.AsyncHttpz(self.auth).poolConnection({"equal":False,
      "limit":limit,
      "sort":"FromMax",
      "username":userUsername,
      "profile_id":profileID
      }, 'searchProfile')

    async def searchinRubino(self, username: str, limit: int = 50, profileID = None):
      userUsername = False

      if username.startswith("@"):
        userUsername = username.replace("@", "")
      else:userUsername = username

      return await httpz.AsyncHttpz(self.auth).poolConnection({"equal":False,
      "limit":limit,
      "sort":"FromMax",
      "username":userUsername,
      "profile_id":profileID
      }, 'searchProfile')

    async def getHashTagTrend(self, limit: int = 50, profileID = None):

      return await httpz.AsyncHttpz(self.auth).poolConnection({

        "equal":False,
        "limit":limit,
        "sort":"FromMax",
        "profile_id":profileID}, "getHashTagTrend")

    async def searchHashTag(self, content: str, limit: int = 50, profileID = None):

      return await httpz.AsyncHttpz(self.auth).poolConnection({
        "content":content,
        "equal":False,"limit":limit,
        "sort":"FromMax",
        "profile_id":profileID}, "searchHashTag")

    async def getPostsByHashTag(self, hashtag: str, limit: int = 51, profileID = None):

      return await httpz.AsyncHttpz(self.auth).poolConnection({

        "equal":False,
        "hashtag": hashtag,
        "limit":limit,
        "profile_id":profileID}, 'getPostsByHashTag')
    
    async def getUserInfoByPostLink(self, link: str):
        postLinkInfo = self.getPostByLink(link=link)
        return postLinkInfo['data']['profile'] if "data" in postLinkInfo.keys() else None

class AsyncRunner(object):
    def runner(obj):
        try:
            asyncio.run(obj)
        except Exception as ERR:
            print(ERR)
            pass

    def runnerUntilComplete(obj):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(obj)
        except DeprecationWarning as DE:
            print(DE)
            pass

class ThreadRubier(object):
    def runner(obj, args: tuple = ()):
        if len(args) == 0:
            try:
                thread = threading.Thread(target=obj)
                thread.start()
            except Exception as ERR:
                print(ERR)
                pass
        else:
            try:
                thread = threading.Thread(target=obj, args=args)
                thread.start()
            except Exception as ERR:
                print(ERR)
                pass

class ThreadRunner(ThreadRubier):
    ...