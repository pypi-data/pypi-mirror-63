#!/usr/bin/env python
# coding: utf-8

# In[85]:


get_ipython().system('pip install matplotlib')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle, ConnectionPatch

def field(ax):
    # size of the pitch is h, w
                h=120
                w=80

                #Pitch Outline & Centre Line

                plt.plot([0,0],[0,w], color="white")
                plt.plot([0,h],[w,w], color="white")
                plt.plot([h,h],[w,0], color="white")
                plt.plot([h,0],[0,0], color="white")
                plt.plot([60,60],[0,w], color="white")

                #Left Penalty Area

                plt.plot([14.6,14.6],[57.8,22.2],color="white")
                plt.plot([0,14.6],[57.8,57.8],color="white")
                plt.plot([0,14.6],[22.2,22.2],color="white")

                #Right Penalty Area
                plt.plot([h,105.4],[57.8,57.8],color="white")
                plt.plot([105.4,105.4],[57.8,22.5],color="white")
                plt.plot([h, 105.4],[22.5,22.5],color="white")

                #Left 6-yard Box
                plt.plot([0,4.9],[48,48],color="white")
                plt.plot([4.9,4.9],[48,32],color="white")
                plt.plot([0,4.9],[32,32],color="white")

                #Right 6-yard Box
                plt.plot([h,115.1],[48,48],color="white")
                plt.plot([115.1,115.1],[48,32],color="white")
                plt.plot([h,115.1],[32,32],color="white")

                #Prepare Circles
                centreCircle = plt.Circle((60,40),8.1,color="white",fill=False)
                centreSpot = plt.Circle((60,40),0.71,color="white")
                leftPenSpot = plt.Circle((9.7,40),0.71,color="white")
                rightPenSpot = plt.Circle((110.3,40),0.71,color="white")

                #Draw Circles
                ax.add_patch(centreCircle)
                ax.add_patch(centreSpot)
                ax.add_patch(leftPenSpot)
                ax.add_patch(rightPenSpot)

                #Prepare Goals
                ax.plot([0,0],[.45*w, .55*w],color='white', linewidth =4)
                ax.plot([h, h],[.45*w, .55*w],color='white', linewidth = 4)

                #Prepare Arcs
                # arguments for arc
                # x, y coordinate of centerpoint of arc
                # width, height as arc might not be circle, but oval
                # angle: degree of rotation of the shape, anti-clockwise
                # theta1, theta2, start and end location of arc in degree
                leftArc = Arc((9.7,40),height=16.2,width=16.2,angle=0,theta1=310,theta2=50,color="white")
                rightArc = Arc((110.3,40),height=16.2,width=16.2,angle=0,theta1=130,theta2=230,color="white")
                left_bottom = Arc((0,0),height=.05*h, width=0.05*h,angle=270,theta1=90,theta2=180,color="white",zorder=5)
                left_top = Arc((0,w),height=.05*h, width=0.05*h,angle=0,theta1=270,theta2=0,color="white",zorder=5)
                right_bottom = Arc((h,0),height=.05*h, width=0.05*h,angle=0,theta1=90,theta2=180,color="white",zorder=5)
                right_top = Arc((h,w),height=.05*h, width=0.05*h,angle=90,theta1=90,theta2=180,color="white",zorder=5)

                #Draw Arcs
                ax.add_patch(leftArc)
                ax.add_patch(rightArc)    
                ax.add_patch(left_bottom)
                ax.add_patch(left_top)
                ax.add_patch(right_bottom)
                ax.add_patch(right_top)

                ax.set_aspect("equal")
                ax.axis("off")

class soccer():
    
    def plot(self,color):
            
        fig=plt.figure()
        self.color=fig.patch.set_facecolor(color)
        fig.set_size_inches(13.5, 9)
        ax=fig.add_subplot(1,1,1)
        
        return field(ax)

