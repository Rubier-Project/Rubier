import rubier.randomStream as randomStream

class RubinoApi(object):
    apis = [
        "https://rubino1.iranlms.ir/", "https://rubino2.iranlms.ir/",
        "https://rubino3.iranlms.ir/", "https://rubino4.iranlms.ir/",
        "https://rubino5.iranlms.ir/", "https://rubino6.iranlms.ir/",
        "https://rubino7.iranlms.ir/", "https://rubino8.iranlms.ir/",
        "https://rubino9.iranlms.ir/", "https://rubino10.iranlms.ir/",
        "https://rubino11.iranlms.ir/", "https://rubino12.iranlms.ir/",
        "https://rubino13.iranlms.ir/", "https://rubino14.iranlms.ir/",
        "https://rubino15.iranlms.ir/", "https://rubino16.iranlms.ir/",
        "https://rubino17.iranlms.ir/", "https://rubino18.iranlms.ir/",
        "https://rubino19.iranlms.ir/", "https://rubino20.iranlms.ir/",
        "https://rubino21.iranlms.ir/", "https://rubino22.iranlms.ir/",
        "https://rubino23.iranlms.ir/", "https://rubino24.iranlms.ir/",
        "https://rubino25.iranlms.ir/", "https://rubino26.iranlms.ir/",
        "https://rubino27.iranlms.ir/", "https://rubino28.iranlms.ir/",
        "https://rubino29.iranlms.ir/", "https://rubino30.iranlms.ir/"
    ]

    def getApi() -> str:
        return randomStream.Stream.choiceStream(RubinoApi.apis)
