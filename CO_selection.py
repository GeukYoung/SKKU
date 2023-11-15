import numpy as np
import matplotlib.pyplot as plt

def FindEnableCO(CO, t_CO, Visible=False):
    th_CO = 0.05  # th of CO change in window
    wt = 12  # window size: 12 min for CO delay
    wt_datenum = 12/24/60 # convert datenumber 12(min)/24(h)/60(min)

    sel_CO = [] # result (logical)
    rel_dCO = [] # for display
    mov_max = [] # for display
    mov_min = [] # for display

    # window sampling (find start index of each window/stride=1)
    cnt_post = 0
    for cnt in range(len(CO)):
        while True:
            if t_CO[cnt] + wt_datenum <= t_CO[cnt_post]:
                CO_error = (np.max(CO[cnt:cnt_post]) - np.min(CO[cnt:cnt_post])) / np.mean(CO[cnt:cnt_post])
                sel_CO.append(CO_error < th_CO)
                if Visible:
                    rel_dCO.append(CO_error)
                    mov_max.append(np.max(CO[cnt:cnt_post]))
                    mov_min.append(np.min(CO[cnt:cnt_post]))
                break
            else:
                if cnt_post >= len(CO)-1:
                    sel_CO.append(False)
                    break
                else:
                    cnt_post += 1

    if Visible:
        plt.subplot(311)
        plt.plot(t_CO, CO, '.')
        plt.plot(t_CO[:len(mov_max)], mov_max)
        plt.plot(t_CO[:len(mov_min)], mov_min)
        plt.ylabel('CO (L/min)')
        plt.xticks([])
        plt.subplot(312)
        plt.plot(t_CO[:len(rel_dCO)], rel_dCO)
        plt.ylabel('error')
        plt.xticks([])
        plt.subplot(313)
        plt.plot(t_CO, CO, '.')
        plt.plot(t_CO[sel_CO], CO[sel_CO], 'r.')
        plt.ylabel('CO (L/min)')
        plt.show()

    return sel_CO

CO_raw = np.load("C:/.../CO_10409339_220611.npy")
CO, t_CO = CO_raw[0, :], CO_raw[1, :]
sel_CO = FindEnableCO(CO,t_CO,True)
