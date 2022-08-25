import glob
import gzip
import retro
import os
from matplotlib.pyplot import imshow, figure

retro.data.Integrations.add_custom_path(
        os.path.join('/home/hyruuk/GitHub/neuromod/mario3.stimuli/')
)
for state_file in sorted(glob.glob('./*pre.state')):
    print(state_file)
    env = retro.make(game='SuperMarioBros3-Nes', record='.')
    print(state_file.split(os.sep)[-1])
    env.load_state(str(state_file.split(os.sep)[-1]),inttype=retro.data.Integrations.CUSTOM_ONLY)
    env.reset()
    # press the button to go in level from overworld
    if 'Wandering' in state_file:# or 'Airship' in state_file:
        # enter the level by moving in the overworld
        for i in range(60):
            obs=env.step([False]*4+[True]+[False]*7)
    elif "Airship" in state_file:
        # Enter the level
        obs=env.step([False]*8+[True]+[False]*3)
        # Wait for the anim to start
        while obs[3]['level_entrance']==0:
            obs=env.step([False]*12)
        # Wait for the anim to stop
        while obs[3]['level_entrance']!=0:
            obs=env.step([False]*12)
    else:
        obs=env.step([False]*8+[True]+[False]*3)
    # step until the timer is starting
    while obs[3]['timer_100']==0:
        obs=env.step([False]*12)
        #print(obs[3]['timer_100'])
    # step until the screen is starting to fade-in (optional)
    while obs[0].sum()==0:
        obs=env.step([False]*12)
    # save the final state
    #figure(state_file.split(os.sep)[-1])
    #imshow(obs[0])
    with gzip.open(state_file.replace('.pre.','.'),'wb') as fh:
        fh.write(env.em.get_state())
    env.close()
