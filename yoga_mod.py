#!/usr/local/env python

# ============== CONFIG PARAMETERS
# ============== INTERNAL LIBRARIES
# ============== EXTERNAL LIBRARIES

def stretch_Spinal():
	Popen(['say', '-v', 'lee', 'Sit cross-legged.'])
	time.sleep(5)
	i = 0
	while i < 2:
		Popen(['say', '-v', 'lee', 'Twist left.'])
		time.sleep(10)
		Popen(['say', '-v', 'lee', 'Return to center.'])
		time.sleep(5)
		Popen(['say', '-v', 'lee', 'Twist right.'])
		time.sleep(10)
		Popen(['say', '-v', 'lee', 'Return to center.'])
		time.sleep(5)
		i += 1;
	Popen(['say', '-v', 'lee', 'Put your left hand on the floor. Inhale. Raise your right arm. While exhaling, reach left.'])
	time.sleep(10)
	Popen(['say', '-v', 'lee', 'Inhale, and relax a moment.'])
	time.sleep(5)
	Popen(['say', '-v', 'lee', 'Exhale and reach left, again.'])
	time.sleep(10)
	Popen(['say', '-v', 'lee', 'Time to switch.'])
	time.sleep(5)
	Popen(['say', '-v', 'lee', 'Put your right hand on the floor. Inhale. Raise your left arm. While exhaling, reach right.'])
	time.sleep(10)
	Popen(['say', '-v', 'lee', 'Inhale, and relax a moment.'])
	time.sleep(5)
	Popen(['say', '-v', 'lee', 'Exhale and reach right, again.'])
	time.sleep(10)

def stretch_Cat():
	Popen(['say', '-v', 'lee', 'Come to all fours'])
	time.sleep(5)
	i = 0
	while i < 3:
		Popen(['say', '-v', 'lee', 'Curve your back toward the ceiling. Drawing your chin to your stomach.'])
		time.sleep(10)
		Popen(['say', '-v', 'lee', 'Inhale deeply'])
		time.sleep(5)
		Popen(['say', '-v', 'lee', 'Exhale and arch your back.'])
		time.sleep(5)
		Popen(['say', '-v', 'lee', 'Slowly raise your head to the ceiling.'])
		time.sleep(5)
		i += 1

def stretch_Lunge():
	Popen(['say', '-v', 'lee', 'Come to all fours'])
	time.sleep(5)
	i = 0
	while i < 3:
		Popen(['say', '-v', 'lee', 'Lunge with your right foot'])
		time.sleep(5)
		Popen(['say', '-v', 'lee', "Don't forget to breathe."])
		time.sleep(5)
		Popen(['say', '-v', 'lee', 'Lunge with left foot.'])
		time.sleep(10)
		i += 1

def fuckGreg2():
	setVolume(3)
	Popen(['say', '-v', 'lee', "I've been instructed to try to further motivate you, " + NAME + "."])
	time.sleep(5)
	Popen(['say', '-v', 'lee', 'Now for a real exercise. Stretching.'])
	time.sleep(5)
	stretch_Spinal()
	stretch_Cat()
	stretch_Lunge()
	Popen(['say', '-v', 'lee', random.choice(POSITIVE) + 'All done. I hope that woke you up.'])
