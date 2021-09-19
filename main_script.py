import EnvironmentLoader

if __name__ == "__main__":
    draw_frame = True
    env = EnvironmentLoader.EnvironmentLoader()
    env.load("env file")

    num_frames = 1

    for i in range(num_frames):
        # env.update()
        if draw_frame:
            print(f'drawing environment')
