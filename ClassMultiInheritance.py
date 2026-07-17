class Engine:
    def start_engine(self):
        print("Engine started")

    def identify(self):
        print("Engine started")

class Radio:
    def play_music(self):
        print("Playing music")

    def identify(self):
        print("Radio plays")



class Car(Engine, Radio):
    pass

car = Car()
car.start_engine()  # inherited from Engine
car.play_music()    # inherited from Radio

Engine.identify(car)
Radio.identify(car)

