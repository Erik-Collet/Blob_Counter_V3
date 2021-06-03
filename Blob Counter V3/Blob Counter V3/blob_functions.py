import numpy as np
import imageio
import matplotlib.pyplot as plt
from math import sqrt
from skimage import feature
import os, xlwt
from xlwt import Workbook
import useability

config = useability.get_config()   
counts = []

#excel stuff
wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')
sheet1.write(0,0, 'Image')
sheet1.write(0,1, 'Total Hits')
sheet1.write(0,2, 'Refined Hits')
sheet1.write(0,3,'Avg Diameter')
start_num = 0

def write_to_excel(pic_num,new,sig_lst,filename,img,sig_ave,list):
    global start_num
    work_num = (start_num*3)+5
    sheet1.write(pic_num+1,0, filename)
    sheet1.write(pic_num+1,1, len(img))
    sheet1.write(pic_num+1,2, len(new))
    sheet1.write(pic_num+1,3, sig_ave)

    sheet1.write(0,work_num+1, filename)
    sheet1.write(1,work_num,'blob_x')
    sheet1.write(1,work_num+1,'blob_y')
    sheet1.write(1,work_num+2,'blob_diam')
    for g in range(len(new)):
        sheet1.write(g+2,work_num,new[g][0])
        sheet1.write(g+2,work_num+1,new[g][1])
        sheet1.write(g+2,work_num+2,sig_lst[g])
    start_num+=1

def run_two_detection(pic_num, files, pic_in, pic_out):
    filename = files[pic_num]
    filename = files[pic_num]
    peep = "Beginning Analysis of " + filename
    print(peep)


    ##FOR DEBLURRED: THRESHOLD 0.01 WORKS GREAT
    fileloc = pic_in + filename
    face = imageio.imread(fileloc, pilmode = 'L')
    pic_height = len(face)/100
    pic_width = len(face[0])/100
    #print(pic_height)
    #print(pic_width)
    img = feature.blob_log(face, min_sigma = config['min_siga'], max_sigma= config['max_siga'], 
                           overlap = config['overlapa'], threshold=config['thresholda'],
                           log_scale = config['log_scalea'])
    img2 = feature.blob_log(face, min_sigma = config['min_sigb'], max_sigma= config['max_sigb'], 
                           overlap = config['overlapb'], threshold=config['thresholdb'],
                           log_scale = config['log_scaleb'])
    toss_num = config['toss_num']
    print("Finished Analaysis")
    face = imageio.imread(fileloc, pilmode = 'RGBA')
    newpic = face
    #Changes to radii
    img[:,2] = img[:,2] *sqrt(2)
    img2[:,2] = img2[:,2] *sqrt(2)

    #Remove excess blobs and print resluts
    new = []
    new2 = []
    tossed = []
    tossed2 = []

    for i in range(len(img)):
        x = int(img[i][0])
        y = int(img[i][1])
        if face[x,y][0]<=toss_num:
            tossed.append(img[i])
        else:
            new.append(img[i])
    for i in range(len(img2)):
        x = int(img2[i][0])
        y = int(img2[i][1])
        if face[x,y][0]<=toss_num:
            tossed2.append(img2[i])
        else:
            new2.append(img2[i])

    big_chk =[]
    big_cir = []
    big_stuff = []
    big_out = []
    for q in range(len(new)):
        if new[q][2] >=7:
            rad = round(new[q][2],0)
            rad = int(rad)
            x = int(new[q][0])
            y = int(new[q][1])
            if x-rad>0:
                startx = x-rad
            elif x-rad<=0:
                startx = 0
            if y-rad>0:
                starty = y-rad
            elif y-rad<=0:
                starty = 0
            endx = x+rad
            endy = y+rad
            area = rad * rad
            for i in range(startx, endx):
                for j in range(starty, endy):
                    if (((i-x)*(i-x))+((j-y)*(j-y))<=(area)):
                        big_cir.append([i,j])
                        big_stuff.append([x,y])
                        if [x,y,rad] not in big_out:
                            big_out.append([x,y,rad])
   
    lils=[]
    final = []
    for i in range(len(new2)):
        if new2[i][2] == sqrt(2)*3:
            pass
        else:
            newx = int(new2[i][0])
            newy = int(new2[i][1])
            poop2 = [newx,newy]
            for j in range(len(big_cir)):
                bigx = big_cir[j][0]
                bigy = big_cir[j][1]
                poopy = [bigx,bigy]
                if poop2 == poopy:
                    final.append(new2[i])
                    lils.append(new2[i])
                    big_chk.append(big_stuff[j])

    for i in range(len(new2)):
        if new2[i][2] == sqrt(2)*3:
            pass
        else:
            newx = int(new2[i][0])
            newy = int(new2[i][1])
            poop2 = [newx,newy]
            for j in range(len(big_cir)):
                bigx = big_cir[j][0]
                bigy = big_cir[j][1]
                poopy = [bigx,bigy]
                if poop2 == poopy:
                    final.append(new2[i])
                    lils.append(new2[i])
                    big_chk.append(big_stuff[j])

    print(lils)

    for i in range(len(new)):
        newx = int(new[i][0])
        newy = int(new[i][1])
        poop = [newx,newy]
        if poop in lils:
            pass
        elif poop not in big_chk:
            final.append(new[i])
        
    print("Total Detections:")
    print(len(img))
    print("Refined:")
    print(len(new))
    
    sig_lst = []
    for i in range(len(final)):
        diameter = 2*((final[i][2])*config['uM_scale'])/config['pix_scale']
        sig_lst.append(diameter)
    sig_ave = 0
    for i in range(len(sig_lst)):
        sig_ave += sig_lst[i]
    sig_ave = round(sig_ave/len(sig_lst),3)
    ave = "final average:" + str(sig_ave)
    print(ave)
    
    tname = ''
    outname = ''
    for i in range(0,len(filename)):
        if filename[i] == '.':
            outname = outname + tname
        tname = tname + filename[i]

    fileout = pic_out + outname + ' output.png'

    txt1 = "Image " + str(pic_num) + ":\n"
    txt2 = "Total hits: " + str(len(img)) +"\n"
    txt3 = "Refined hits: " + str(len(final)) + "\n"
    txt5 = "Average Diameter (microns): " + str(sig_ave) +"\n\n"
    txt4 = txt1 + txt2 + txt3 + txt5

    counts.append(txt4)

    write_to_excel(pic_num,final,sig_lst,filename,
                   img,sig_ave,list)

    fig = plt.figure(filename,frameon = False)
    fig.set_size_inches(pic_width, pic_height)
    ax = plt.Axes(fig, [0.,0.,1.,1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    for blob in big_out:
        ax.imshow(face)
        y, x, r = blob
        c = plt.Circle((x,y), r, color = 'blue', linewidth = 1, fill = False)
        ax.add_patch(c)
        ax.set_axis_off()
    for blob in final: 
        ax.imshow(face)
        y, x, r = blob
        c = plt.Circle((x,y), r, color = 'red', linewidth = 1, fill = False)
        ax.add_patch(c)
        ax.set_axis_off()
    fig.savefig(fileout, dpi = 100)
    fig.title = filename
    plt.tight_layout()
    plt.show()

def run_one_detection(pic_num, files, pic_in, pic_out):
    filename = files[pic_num]
    peep = "Beginning Analysis of " + filename
    print(peep)

    ##FOR DEBLURRED: THRESHOLD 0.01 WORKS GREAT
    fileloc = pic_in + filename 
    face = imageio.imread(fileloc, pilmode = 'L')
    pic_height = len(face)/100
    pic_width = len(face[0])/100

    img = feature.blob_log(face, min_sigma = config['min_siga'], max_sigma= config['max_siga'], 
                           overlap = config['overlapa'], threshold=config['thresholda'],
                           log_scale = config['log_scalea'])
    toss_num = config['toss_num']
    print("Finished Analaysis")
    face = imageio.imread(fileloc, pilmode = 'RGBA')
    newpic = face
    #Changes to radii
    img[:,2] = img[:,2] *sqrt(2)

    #Remove excess blobs and print resluts
    new = []
    tossed = []

    for i in range(len(img)):
        x = int(img[i][0])
        y = int(img[i][1])
        if face[x,y][0]<=toss_num:
            tossed.append(img[i])
        else:
            new.append(img[i])
        
    print("Total Detections:")
    print(len(img))
    print("Refined:")
    print(len(new))
    
    sig_lst = []
    for i in range(len(new)):
        diameter = 2*((new[i][2])*config['uM_scale'])/config['pix_scale']
        sig_lst.append(diameter)
    sig_ave = 0
    for i in range(len(sig_lst)):
        sig_ave += sig_lst[i]
    sig_ave = round(sig_ave/len(sig_lst),3)
    ave = "final average:" + str(sig_ave)
    print(ave)

    tname = ''
    outname = ''
    for i in range(0,len(filename)):
        if filename[i] == '.':
            outname = outname + tname
        tname = tname + filename[i]

    fileout = pic_out + outname + ' output.png'

    txt1 = "Image " + str(pic_num) + ":\n"
    txt2 = "Total hits: " + str(len(img)) +"\n"
    txt3 = "Refined hits: " + str(len(new)) + "\n"
    txt5 = "Average Diameter (microns): " + str(sig_ave) +"\n\n"
    txt4 = txt1 + txt2 + txt3 + txt5

    counts.append(txt4)

    write_to_excel(pic_num,new,sig_lst,filename,
                   img,sig_ave,list)

    fig = plt.figure(filename,frameon = False)
    fig.set_size_inches(pic_width, pic_height)
    ax = plt.Axes(fig, [0.,0.,1.,1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    for blob in new:
        ax.imshow(face)
        y, x, r = blob
        c = plt.Circle((x,y), r, color = 'red', linewidth = 1, fill = False)
        ax.add_patch(c)
        ax.set_axis_off()
    for blob in tossed:
        ax.imshow(face)
        y, x, r = blob
        c = plt.Circle((x,y), r, color = 'blue', linewidth = 1, fill = False)
        ax.add_patch(c)
        ax.set_axis_off()
    fig.savefig(fileout, dpi = 100)
    fig.title = filename
    plt.tight_layout()
    plt.show()

