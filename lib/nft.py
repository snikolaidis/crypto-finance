import json, uuid, random, math, shutil, os, time
from PIL import Image
from lib import globals

class Nft:

    configuration = []
    numberOfImagesGenerated = 0

    def __init__(self):
        random.seed()


    def openTheConfigurationFile(self):
        try:
            f = open('./config/nft.json',)
            self.configuration = json.load(f)
            return True
        except:
            return False


    def __generateAllCombinationsFunc(self, layerNo, filename = ''):
        for i in range(self.configuration["layers"][layerNo]["common"]):
            if filename == '':
                newFilename = self.configuration["layers"][layerNo]["name"] + "|" + str(i + 1)
            else:
                newFilename = filename + "~" + self.configuration["layers"][layerNo]["name"] + "|" + str(i + 1)

            if layerNo == len(self.configuration["layers"]) - 1:
                self.numberOfImagesGenerated += 1
                if self.numberOfImagesGenerated % 100 == 0:
                    print(str(self.numberOfImagesGenerated) + "...")
                globals.database.execSQL("INSERT INTO nft_all_conbinations(code, uuid, used, used_date, uncommon_id) values (?,?,0,null,0)", [newFilename, str(uuid.uuid1())])
            else:
                self.__generateAllCombinationsFunc(layerNo + 1, newFilename)
    

    # 1. Retrieves a random un-used record from all combinations
    # 2. Checks if it will have uncommon (or rare) features
    # 3. Generates the necessary image file
    # 4. Updates the database accordingly
    def __pickAFile(self):
        # How many images are unselected?
        cntNotUsed, = globals.database.execSelectOne("SELECT COUNT(*) cnt FROM nft_all_conbinations WHERE used = 0")
        # Pick a random one
        randomImageID = math.floor(cntNotUsed * random.random())
        # Time to get the image
        image_id, image_code, image_uuid = globals.database.execSelectOne("SELECT id, code, uuid FROM nft_all_conbinations WHERE used = 0 LIMIT 1 OFFSET ?", [randomImageID])

        image_filename = image_uuid + ".png"
        image_filenameFull = "./images/nft/output/" + image_filename

        # If the file exists, delete it and we will re-create it
        if os.path.exists(image_filenameFull):
            os.remove(image_filenameFull)

        # We copy the card.png file to the destination, using the uuid as a name
        shutil.copyfile("./images/nft/layers/card.png", image_filenameFull)
        main_image = Image.open(image_filenameFull).convert("RGBA")

        # Split the code in chuncks, to get all layers
        layers = image_code.split("~")
        for layer in layers:
            layerInfo = layer.split("|")
            layer_filename = layerInfo[0] + '-common-' + layerInfo[1] + '.png'
            layer_filenameFull = "./images/nft/layers/" + layer_filename
            layer_image = Image.open(layer_filenameFull).convert("RGBA")

            # ToDo: Checks if it will have uncommon (or rare) features

            main_image = Image.alpha_composite(main_image, layer_image)

            # main_image.paste(main_image, (0, 0), layer_image)

        # Finally, save the new file and update the database
        main_image.save(image_filenameFull, "PNG")
        globals.database.execSQL("UPDATE nft_all_conbinations SET used = ?, used_date = ? WHERE id = ?", [1, time.strftime('%Y-%m-%d %H:%M:%S'), image_id])

        return (image_id, image_code, image_filename)


    def generateAllCombinations(self):
        if self.openTheConfigurationFile() == False:
            print("Please make sure file ./config/nft.json exists and has the correct structure")
        
        dir = "./images/nft/output"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        globals.database.execSQL("DELETE FROM nft_all_conbinations")
        globals.database.execSQL("DELETE FROM nft_uncommon_conbinations")

        print("Building all combinations")

        self.numberOfImagesGenerated = 0
        self.__generateAllCombinationsFunc(0)

        cnt, = globals.database.execSelectOne("SELECT COUNT(*) cnt FROM nft_all_conbinations")
        print("Total combinations created: " + str(cnt))
    

    def selectRandomImages(self):
        numberOfImages = globals.tools.pickAnInteger(message = "Give me the number of images you want to generate", max = 10_000)
        for i in range(numberOfImages):
            print("Generating file no." + str(i + 1))
            generatedFileInfo = self.__pickAFile()
            print(generatedFileInfo)