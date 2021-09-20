from EnvironmentLoader import EnvironmentLoader

if __name__ == "__main__":
    draw_frame = True
    env = EnvironmentLoader()
    env_mediator = env.load("env file")

    num_frames = 10

    for i in range(num_frames):
        env_mediator.request_frame()
        if draw_frame:
            print(f'drawing environment')
