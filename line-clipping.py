'''
Computer Graphics using OpenGL
Sutherland-Cohen Line Clipping Algorithm
Author:
	Shivika Sharma
This script inputs two end points using a mouse input as well as the virtual window 
and clips the line according to this window.
'''

#Importing the required header files
from os import stat
from OpenGL.GL import*
from OpenGL.GLU import*
from OpenGL.GLUT import*
import sys

#Initialising the window
#Setting window colour background as white
def myInit():
	glClearColor(1,1,1,1)       
	glColor3f(0,1,1)           
	glPointSize(5.0)           
	gluOrtho2D(0, 500, 0, 500) 

#Global variables of Height and width of window
height = 500
width = 500


#Resize function preserves the aspect ratio in case the user resizes the window
def resize(w,h):
	#Since we are using height and widths in dimensions of figures to be drawn, it mustn't be 0
	if w == 0:
		w = 1
	
	if h == 0:
		h = 1

	global width, height

	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()

	width = w
	height = h

	glOrtho(0, w, 0, h,-1.0, 1.0)

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	pass

#Initialising user specified window's corner points as global variables
x_min = 0
x_max = 0
y_min = 0
y_max = 0

#Checks if the button is pressed for creating a user window or specifying line end points
primitive = None

#List to store points
given_points = []



#Specifying a point class
#Each point has x and y coordinates
#In addition, each point also has its bitcode attribute according to Sutherland-Cohen algorithm
class point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.bitcode = [ ]
		self.find_bitcode()
	
	def print_point(self):
		print("The x coordinate is: ", self.x)
		print("The y coordinate is: ", self.y)

	def find_bitcode(self):
		self.bitcode = []
		if self.y>y_max:
			self.bitcode.append(1)
		else:
			self.bitcode.append(0)
		
		if self.y<y_min:
			self.bitcode.append(1)
		else:
			self.bitcode.append(0)

		if self.x>x_max:
			self.bitcode.append(1)
		else:
			self.bitcode.append(0)

		if self.x<x_min:
			self.bitcode.append(1)
		else:
			self.bitcode.append(0)

	
	def print_bitcode(self):
		print(self.bitcode)


#Initialising 4 global points for use in later functions
end_point_1 = point(0,0)
end_point_2 = point(0,0)
end_point_3 = point(0,0)
end_point_4 = point(0,0)



#This function returns the bitcode of the bitwise AND of the bitcodes of the two given end points of the line
def check_point( end_point_1, end_point_2):
	answer = [0,0,0,0]
	for i in range(4):
		if ((end_point_2[i]==0 or end_point_1[i]==0)):
			answer[i] = 0
		else:
			answer[i] = 1 
	return answer

#This function is used to calculate the ax + by + c=0 of a line
def find_slope(end_point_1,end_point_2):
	a = end_point_2.y - end_point_1.y
	b = end_point_2.x - end_point_1.x
	c = (end_point_2.x * end_point_1.y) - (end_point_1.x * end_point_2.y)
	return a, b, c

#This function checks if the bitwise AND of the bitcodes of the two points results in a trivially rejected line
#Returns -1 is line is trivially rejected
#Returns 1 if line is trivially accepted
def check_trivial_reject(ans):
	for element in ans:
		if element==1:
			return -1
	return 1

#This function finds the intersection point of a given line (given endpoints) and a vertical boundary
def find_intersection_y(end_point_1,end_point_2,y_boundary):
	a, b, c = find_slope(end_point_1,end_point_2)
	try:
		x_changed = (-b*y_boundary + c)/(-a)
	#If a = 0, it would give than error. The point would simply not change since it is on a horizontal line
	except:
		x_changed = end_point_1.x
	new_point = point(x_changed,y_boundary)
	return new_point

#This function finds the intersection point of a given line (given endpoints) and a horizontal boundary
def find_intersection_x(end_point_1,end_point_2,x_boundary):
	print(end_point_2.x,end_point_2.y)
	a, b, c = find_slope(end_point_1,end_point_2)
	print(a,b,c)
	try:
		y_changed = (a*x_boundary + c)/b
	#If b = 0, it would give than error. The point would simply not change since it is on a vertical line
	except:
		y_changed = end_point_1.y
		print(y_changed)
	new_point = point(x_boundary,y_changed)
	return new_point

#This function clips the line in the required user specified window
#It returns the end points of the clipped line
#After each change the function checks if the line is trivially rejected
def clip_line(end_point_1,end_point_2):
	trivial_check = check_point(end_point_1.bitcode,end_point_2.bitcode)
	if check_trivial_reject(trivial_check)==-1:
		print("The line was trivially rejected")
		return None, None

	#This flag variable checks if both the end point bitcodes are 0
	#If flag==1 we return the same endpoints as no clipping is required
	flag = 1
	for element in end_point_1.bitcode:
		if element==1:
			flag = -1

	for element in end_point_2.bitcode:
		if element==1:
			flag = -1

	#If no endpoint bitcode is non-zero, we trivially accept the line.
	if flag==1:
		print("The line was trivially accepted")
		return end_point_1,end_point_2


	if (end_point_1.y > y_max):
		end_point_1 = find_intersection_y(end_point_1,end_point_2,y_max)
		trivial_check = check_point(end_point_1.bitcode,end_point_2.bitcode)
		if check_trivial_reject(trivial_check)==-1:
			end_point_1.find_bitcode()
			print("The line was trivially rejected")
			return None, None

	if (end_point_2.y > y_max):
		end_point_2 = find_intersection_y(end_point_2,end_point_1,y_max)
		trivial_check = check_point(end_point_1.bitcode,end_point_2.bitcode)
		if check_trivial_reject(trivial_check)==-1:
			end_point_2.find_bitcode()
			print("The line was trivially rejected")
			return None, None

	if (end_point_1.y < y_min):
		end_point_1 = find_intersection_y(end_point_1,end_point_2,y_min)
		trivial_check = check_point(end_point_1.bitcode,end_point_2.bitcode)
		if check_trivial_reject(trivial_check)==-1:
			end_point_1.find_bitcode()
			print("The line was trivially rejected")
			return None, None

	if (end_point_2.y < y_min):
		end_point_2 = find_intersection_y(end_point_2,end_point_1,y_min)
		trivial_check = check_point(end_point_1.bitcode,end_point_2.bitcode)
		if check_trivial_reject(trivial_check)==-1:
			end_point_2.find_bitcode()
			print("The line was trivially rejected")
			return None, None

	if (end_point_1.x > x_max):
		end_point_1 = find_intersection_x(end_point_1,end_point_2,x_max)
		trivial_check = check_point(end_point_1.bitcode,end_point_2.bitcode)
		if check_trivial_reject(trivial_check)==-1:
			end_point_1.find_bitcode()
			print("The line was trivially rejected")
			return None, None

	if (end_point_2.x > x_max):
		end_point_2 = find_intersection_x(end_point_2,end_point_1,x_max)
		trivial_check = check_point(end_point_1.bitcode,end_point_2.bitcode)
		if check_trivial_reject(trivial_check)==-1:
			end_point_2.find_bitcode()
			print("The line was trivially rejected")
			return None, None

	if (end_point_1.x < x_min):
		end_point_1 = find_intersection_x(end_point_1,end_point_2,x_min)
		trivial_check = check_point(end_point_1.bitcode,end_point_2.bitcode)
		if check_trivial_reject(trivial_check)==-1:
			end_point_1.find_bitcode()
			print("The line was trivially rejected")
			return None, None

	if (end_point_2.x < x_min):
		end_point_2 = find_intersection_x(end_point_2,end_point_1,x_min)
		trivial_check = check_point(end_point_1.bitcode,end_point_2.bitcode)
		if check_trivial_reject(trivial_check)==-1:
			end_point_2.find_bitcode()
			print("The line was trivially rejected")
			return None, None

	print("The line has been clipped")
	end_point_1.print_point()
	end_point_2.print_point()
	clipped_points = [end_point_1]+[end_point_2]
	return end_point_1,end_point_2


#This function is used to get the user mouse inputs
def get_mouse_inputs(button, state, x, y):
	global height, width
	
	if (button == GLUT_LEFT_BUTTON) and (state == GLUT_DOWN):

		global x_max,x_min,y_max,y_min, given_points, primitive, end_point_2, end_point_1, end_point_4, end_point_3

		#(x,y) should be coordinates that we use in endpoint coordinates/ corner points of user window
		y = height - y
		print(x,y)


		#Updating primitive value if needed
		if x <= (0.1 * width):

			if y >= (0.9 * height):
				#If the state was previously 'points', we make the line endpoints (3&4) = 0
				if primitive=='points':
					end_point_3 = point(0,0)
					end_point_4 = point(0,0)
				primitive = 'window'
				given_points = []
				
			elif y >= (0.8 * height):
				#If the state was previously 'window', we make the user window endpoints (1&2) = 0
				if primitive=='window':
					end_point_1 = point(0,0)
					end_point_2 = point(0,0)
				primitive = 'points'
				given_points = []


			
			display()

		
		else:
			#Since any input (for 'window' or 'points') requires a set of 2 points, 
			#we set the given_points list to null if the length becomes more than two.
			
			if len(given_points)<2:
				selected = point(x,y)
				given_points.append(selected)
			else:
				given_points = []
				selected = point(x,y)
				given_points.append(selected)

			#print("The given points list is: ",given_points)


			if (primitive == 'window') and (len(given_points) == 2):
				end_point_1 = point(given_points[0].x,given_points[0].y)
				end_point_2 = point(given_points[1].x,given_points[1].y)
				x_max = max(end_point_1.x,end_point_2.x)
				x_min = min(end_point_1.x,end_point_2.x)
				y_max = max(end_point_1.y,end_point_2.y)
				y_min = min(end_point_1.y,end_point_2.y)
				glColor3f(0,0,0)
				#glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
				#glRectf(x_max,y_min,x_max,y_min)
				given_points = []

			if (primitive == 'points') and (len(given_points) == 2):
				end_point_3 = point(given_points[0].x,given_points[0].y)
				end_point_4 = point(given_points[1].x,given_points[1].y)
		display()
		print("The current user option is: ",primitive)


#This function draws the side menu bar for the user to select options from
def draw_menu_bar():

	global width, height
	pointSize = 5

	#Drawing menu bar horizontal line
	glColor3f(0,0,0)
	glBegin(GL_LINES)
	glVertex3f(0.1*width, 0.0,0.0)
	glVertex3f(0.1*width, height,0.0)
	glEnd()

	#If an option is selected, it becomes dark grey. Else it is light grey.
	

	# First option box
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
	
	if primitive=='window':
		glColor3f(0.2,0.2,0.2)
	else:
		glColor3f(0.5,0.5,0.5)

	glRectf(0,0.9*height, 0.1 * width, height)

	glColor3f(0.0, 0.0, 0.0)
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
	glRectf(0.0, 0.9*height, 0.1*width, height)

	glColor3f(0,0,0)

	#User window option box
	glBegin(GL_LINE_LOOP)
	glVertex3f(0.01*width, 0.91*height, 0.0)
	glVertex3f(0.09*width, 0.91*height, 0.0)
	glVertex3f(0.09*width, 0.99*height, 0.0)
	glVertex3f(0.01*width, 0.99*height, 0.0)
	glEnd()



	#Second option box
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
	
	if primitive=='points':
		glColor3f(0.2,0.2,0.2)
	else:
		glColor3f(0.5,0.5,0.5)

	glRectf(0,0.8*height, 0.1 * width, 0.9*height)

	glColor3f(0.0, 0.0, 0.0)
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
	glRectf(0.0, 0.8*height, 0.1*width, 0.9*height)

	#Drawing clipping option
	glPointSize(pointSize)
	glColor3f(0.0, 0.0, 0.0)
	glBegin(GL_LINES)
	glVertex3f(0.02*width, 0.82*height,0.0)
	glVertex3f(0.08*width, 0.88*height,0.0)

	glVertex3f(0.08*width, 0.82*height,0.0)
	glVertex3f(0.02*width, 0.88*height,0.0)

	glEnd()


#The display function
def display():
	global end_point_1, end_point_2, x_max, x_min, y_max, y_min

	glClear(GL_COLOR_BUFFER_BIT)    
	draw_menu_bar()

	if primitive=='window' or primitive=='points':
	
		glColor3f(0,0,0)
		glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
		glRectf(x_min,y_min,x_max, y_max)

	if primitive=='points':

		glBegin(GL_LINES)
		glColor3f(1,0,0)
		glVertex2f(end_point_3.x, end_point_3.y) 
		glVertex2f(end_point_4.x, end_point_4.y) 
		glEnd()

		#End points 5 and 6 store the endpoints of clipped lines
		end_point_5,end_point_6 = clip_line(end_point_3,end_point_4)
		#If the line is rejected, endpoints 5 and 6 would be none and thus we must check for their existence.
		if end_point_5!=None and end_point_6!=None:
			glBegin( GL_LINES )
			glColor3f(0,1,0)
			glVertex2f(end_point_5.x, end_point_5.y) 
			glVertex2f(end_point_6.x, end_point_6.y)
			glEnd()
	
	glFlush() 


#Specifying system arguments
glutInit(sys.argv)

#Specifying buffer frame
glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)


#Setting window size and position
glutInitWindowSize(500,500)
glutInitWindowPosition(100,100)

#Adding window title
glutCreateWindow("Line Clipping Window")

#Initiating window specifications
myInit()

#Instantiating mouse inputs
glutMouseFunc(get_mouse_inputs)

#Calling glut display and resize functions to preserve aspect ratio
glutReshapeFunc(resize)
glutDisplayFunc(display)


#To keep the window open continuously
glutMainLoop()

