const { NetworkHandler, Random, StringBuilder} = require("./toolkit");
const axiosClass = require('axios');
const fs = require("fs");

class Rubier{
    constructor(auth, Proxy){
        this.auth = auth;
        this.proxy = Proxy ? Proxy : undefined || null;
        this.network = new NetworkHandler(this.auth, this.proxy);
    }

    addPostViewCount({
        postId = null,
        postProfileId = null,
        callback = null
    } = {}){
        this.network.create("addPostViewCount", {
            "post_id": postId,
            "post_profile_id": postProfileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    addStoryViewCount({
        profileId = null,
        storyId = null,
        storyProfileId = null,
        callback = null
    } = {}){
        this.network.create("addViewStory", {
            "profile_id": profileId,
            "story_ids": [storyId],
            "story_profile_id": storyProfileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    isExistUsername({
        username = null,
        callback = null
    } = {}){
        this.network.create("isExistUsername", {
            "username": username
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    createPage({
        name = "",
        username = `RubierJS_${new Date().getTime()}`,
        bio = "Rubier-NodeJS",
        callback = null
    } = {}){
        this.network.create("createPage", {
            "username": username,
            "name": name,
            "bio": bio
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    sendComment({
        text = "",
        postId = null,
        postProfileId = null,
        profileId = null
    } = {}){
        this.network.create("addComment", {
            "content": text,
            "post_id": postId,
            "post_profile_id": postProfileId,
            "profile_id": profileId,
            "rnd": new Random().getRandomNumber
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getMe({
        callback = null
    } = {}){
        this.network.create("getMyProfileInfo", {"profile_id": null}, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getMyProfileInfo({
        callback = null
    } = {}){
        this.network.create("getMyProfileInfo", {"profile_id": null}, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    followPage({
        followId = null,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("requestFollow", {
            "f_type": "Follow",
            "follow_id": followId,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    unfollowPage({
        followId = null,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("requestFollow", {
            "f_type": "Unfollow",
            "follow_id": followId,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    blockPage({
        blockId = null,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("setBlockProfile", {
            "action": "Block",
            "block_id": blockId,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    unBlockPage({
        blockId = null,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("setBlockProfile", {
            "action": "Unblock",
            "block_id": blockId,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getComments({
        postId = null,
        postProfileId = null,
        limit = 100,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("getComments", {
            "post_id": postId,
            "post_profile_id": postProfileId,
            "limit": limit,
            "profile_id": profileId,
            "sort": "FromMax"
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getPostByLink({
        link = null,
        profileId = null,
        callback = null
    } = {}){
        let newLink = link.replace("https://rubika.ir/post/", "").replace("post/", "");
        this.network.create("getPostByShareLink", {
            "share_string": newLink,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getProfileList({
        limit = 10,
        callback = null
    } = {}){
        this.network.create("getProfileList", {
            "limit": limit,
            "sort": "FromMax",
            "equal": false
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getProfileStories({
        limit = 100,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("getProfileStories", {
            "limit": limit,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getRecentFollowingPosts({
        limit = 30,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("getRecentFollowingPosts", {
            "equal": false,
            "limit": limit,
            "profile_id": profileId,
            "sort": "FromMax"
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getShareLinkFormPost({
        postId = null,
        postProfileId = null,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("getShareLink", {
            "post_id": postId,
            "post_profile_id": postProfileId,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getStoryIds({
        targetProfileId = null,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("getStoryIds", {
            "profile_id": profileId,
            "target_profile_id": targetProfileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    savePost({
        postId = null,
        postProfileId = null,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("postBookmarkAction", {
            "action_type": "Bookmark",
            "post_id": postId,
            "post_profile_id": postProfileId,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    unsavePost({
        postId = null,
        postProfileId = null,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("postBookmarkAction", {
            "action_type": "Unbookmark",
            "post_id": postId,
            "post_profile_id": postProfileId,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    updateProfile({
        profileId = null,
        callback = null
    } = {}){
        this.network.create("updateProfile", {
            "profile_id": profileId,
            "profile_status": "Public"
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    likePost({
        postId = null,
        postProfileId = null,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("likePostAction", {
            "action_type": "Like",
            "post_id": postId,
            "post_profile_id": postProfileId,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    unLikePost({
        postId = null,
        postProfileId = null,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("likePostAction", {
            "action_type": "Unlike",
            "post_id": postId,
            "post_profile_id": postProfileId,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    likeComment({
            commentId = null,
            postId = null,
            profileId = null,
            callback = null
    } = {}){
        this.network.create("likeCommentAction", {
            "action_type": "Like",
            "comment_id": commentId,
            "post_id": postId,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    unLikeComment({
            commentId = null,
            postId = null,
            profileId = null,
            callback = null
        } = {}){
        this.network.create("likeCommentAction", {
            "action_type": "Unlike",
            "comment_id": commentId,
            "post_id": postId,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getSavePosts({
        limit = 10,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("getBookmarkedPosts", {
            "equal": false,
            "limit": limit,
            "profile_id": profileId,
            "sort": "FromMax"
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getArchiveStories({
        limit = 10,
        startId = null,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("getArchiveStories", {
            "equal": false,
            "limit": limit,
            "start_id": startId,
            "profile_id": profileId,
            "sort": "FromMax"
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getProfileHighlights({
        limit = 10,
        maxId = null,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("getProfileHighlights", {
            "equal": false,
            "limit": limit,
            "max_id": maxId,
            "profile_id": profileId,
            "sort": "FromMax"
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getProfileFollowers({
        targetProfileId = null,
        limit = 50,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("getProfileFollowers", {
            "equal": false,
            "f_type": "Following",
            "limit": limit,
            "sort": "FromMax",
            "target_profile_id": targetProfileId,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getMyStories({
        limit = 10,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("getMyStoriesList", {
            "limit": limit,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    deleteStory({
        storyId = null,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("deleteStory", {
            "story_id": storyId,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getExplorePosts({
        topicId = "",
        limit = 50,
        maxId = null,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("getExplorePosts", {
            "equal": false,
            "limit": limit,
            "max_id": maxId,
            "topic_id": topicId,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    searchProfile({
        username = "",
        limit = 50,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("searchProfile", {
            "limit": limit,
            "sort": "FormMax",
            "username": !String(username).startsWith("@") ? username : username.replace("@", ""),
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getHashTagTrend({
        limit = 50,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("getHashTagTrend", {
            "equal": false,
            "limit": limit,
            "sort": "FormMax",
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    searchHashTag({
        hashtag = "",
        limit = 51,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("searchHashTag", {
            "equal": false,
            "hashtag": hashtag,
            "limit": limit,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getPostsByHashtag({
        hashtag = "",
        limit = 51,
        profileId = null,
        callback = null
    } = {}){
        this.network.create("getPostsByHashTag", {
            "equal": false,
            "hashtag": hashtag,
            "limit": limit,
            "profile_id": profileId
        }, (data) => {
            if (callback === null){true;}else{
                callback(data);
            }
        })
    }

    getUserInfoByPostLink({
        link = "",
        callback = null
    } = {}){
        this.getPostByLink({
            link: link,
            callback: (resp) => {
                if (callback === null){true;}else{
                    callback(resp.data.profile);
                }
            }
        })
    }

    getGuidByUsername({
        username = "",
        callback = null
    } = {}){
        this.isExistUsername({
            username: username,
            callback: (userGuid) => {
                if (callback === null){true;}else{
                    callback(userGuid.data.profile.chat_link.open_chat_data.object_guid);
                }
            }
        })
    }

    getProfileIdByUsername({
        username = "",
        callback = null
    } = {}){
        this.isExistUsername({
            username: username,
            callback: (userGuid) => {
                if (callback === null){true;}else{
                    callback(userGuid.data.profile.id);
                }
            }
        })
    }

    getBioByUsername({
        username = "",
        callback = null
    } = {}){
        this.isExistUsername({
            username: username,
            callback: (userGuid) => {
                if (callback === null){true;}else{
                    callback(userGuid.data.profile.bio);
                }
            }
        })
    }

    getNameByUsername({
        username = "",
        callback = null
    } = {}){
        this.isExistUsername({
            username: username,
            callback: (userGuid) => {
                if (callback === null){true;}else{
                    callback(userGuid.data.profile.name);
                }
            }
        })
    }

    requestUploadFile({
        file,
        size = null,
        Type = "Picture",
        profileId = null,
        callback = null
    } = {}){
        let newFilename = new StringBuilder().pathBuild(file);
        let newSize = fs.statSync(file).size;

        this.network.create("requestUploadFile", {
            "file_name": newFilename,
            "file_size": size ? size !== null : newSize,
            "file_type": Type,
            "profile_id": profileId
        }, (dataUpload) => {
            if (callback === null){true;}else{
                callback(dataUpload);   
            }
        })
    }

    uploadSomething({
        file,
        type,
        callback = null
    } = {}){
        if (!String(file).startsWith("https")){
            this.requestUploadFile({file: file, callback: (rubierData) => {
                let respone = rubierData.data;
                let bytes = fs.createReadStream(file);
                let fileId = respone.file_id;
                let fileSize = fs.statSync(file).size;
                let hash = respone.hash_file_request;
                let url = respone.server_url;
                let json_data = {
                    "auth": this.auth,
                    "Host": String(url).replace("https://", "").replace("UploadFile.ashx", ""),
                    "chunk-size": fileSize,
                    "file-id": fileId,
                    "hash-file-request": hash,
                    "content-type": "application/octet-stream",
                    "content-length": fileSize,
                    "accept-encoding": "gzip",
                    "user-agent": "okhttp/3.12.1",
                    "part-number": "1",
                    "total-part": "1"
                }
    
                new axiosClass.Axios("POST").post(url, JSON.stringify(json_data), {
                    data: bytes
                }).then((responez) => {
                    let datas = JSON.parse(responez.data);
                    if (callback === null){true;}else{
                        callback(datas);
                    }
                })
            }})
        }else{
            let newFilename = new StringBuilder().pathBuild(file);
            let newSize = fs.statSync(file).size;
        
            this.network.create("requestUploadFile", {
                "file_name": newFilename,
                "file_size": newSize,
                "file_type": type,
                "profile_id": ""
            }, (dataUpload) => {
                if (callback === null){true;}else{
                    callback(dataUpload);   
                }
            })
        }
    }
}

module.exports = {
    Rubier
}
