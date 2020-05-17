import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from copy import copy
import datetime
from shutil import copyfile


months = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
months_eng = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"]
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 31, 31]

def floatif(arg):
    try:
        return float(arg)
    except:
        return arg.strip()


def load_data(fname):
    data = header = None
    for row in open(fname):
        srow = row.strip()
        if data is None:
            header = [x.strip().lower() for x in srow.split(",")]
            data = {x: [] for x in header}
            continue
        arow = srow.split(",")
        for i, h in enumerate(header):
            data[h].append(floatif(arow[i]))
    return data


size = .15
phi = 90
cc = False

labels = ["ITA", "EUR", "CHN", "USA", "WRD"]
rad_list = [1., 1. - size, 1. - 2*size, 1. - 3*size, 1. - 4*size]
roff_list = [size / 2. + .015, size / 2. + .01, size / 2. + .01, size / 2. + .03, size / 2. + .02]
aoff_list = [np.pi * 4e-2, np.pi * 5e-2, np.pi * 7e-2, np.pi * 8e-2, np.pi * 1.5e-1]
txtcol_list = list("wwwkk")

data = {"ITA": load_data("data/italy.csv"),
        "EUR": load_data("data/europe.csv"),
        "CHN": load_data("data/china.csv"),
        "USA": load_data("data/usa.csv"),
        "WRD": load_data("data/world.csv")}


colors = matplotlib.cm.viridis(np.linspace(0, 1, len(labels)+1))

val_old_list = None
iframe = 0
nframes = 10
for year in data["ITA"]["year"]:
    print(year)

    if val_old_list is None:
        val_old_list = [min(1e0/data[lab]["total"][data[lab]["year"].index(year)], 1e0) for lab in labels]
    else:
        val_old_list = copy(val_target_list)
    val_target_list = [min(1e0/data[lab]["total"][data[lab]["year"].index(year)], 1e0) for lab in labels]

    for jj in range(nframes):
        plt.clf()


        ndays = sum(days)
        rin = 1.
        rout = 1.1
        rout2 = 1.15
        iday = 0
        plt.plot([0, 0], [1-5*size, rout2], color="k", lw=2.)
        for j, d in enumerate(days):
            cos = np.cos(-2. * np.pi * iday / (ndays - 1) + np.pi/2.)
            sin = np.sin(-2. * np.pi * iday / (ndays - 1) + np.pi/2.)
            plt.plot([rin * cos, rout2 * cos],
                [rin * sin, rout2 * sin],
                color="k", lw=1)
            for i in range(d):
                cos = np.cos(-2. * np.pi * iday / (ndays - 1) + np.pi/2.)
                sin = np.sin(-2. * np.pi * iday / (ndays - 1) + np.pi/2.)
                plt.plot([rin * cos, rout * cos],
                    [rin * sin, rout * sin],
                    color="k", lw=.3)
                iday += 1

        # MONTH LABELS
        dtot = 0
        rmout = 1.18
        for i, dd in enumerate(days):
            iday = dtot + dd // 2
            ang = -2. * np.pi * iday / (ndays - 1) + np.pi/2.
            cos = np.cos(ang)
            sin = np.sin(ang)
            plt.text(rmout * cos, rmout * sin, months[i].upper(), rotation=ang / np.pi * 180. - 90.,
                     horizontalalignment='center', verticalalignment='center')
            dtot += dd

        wedges_list = []
        rloff_list = [0, 0.1, 0, 0, 0.1]
        for ii, lab in enumerate(labels):

            rad = rad_list[ii]
            roff = roff_list[ii]
            aoff = aoff_list[ii]
            val_target = val_target_list[ii]
            val_old = val_old_list[ii]
            val = jj * (val_target - val_old) / (nframes - 1) + val_old
            wedges, texts = plt.pie([val, 1e0 - val], radius=rad, colors=[colors[ii], "none"],
                   startangle=phi, counterclock=cc,
                   wedgeprops=dict(width=size*1.05, edgecolor="none"))
            ang = - 2. * np.pi * val + np.pi/2.
            plt.text((rad - roff) * np.cos(ang + aoff),
                     (rad - roff) * np.sin(ang + aoff),
                     lab, color=txtcol_list[ii], rotation=(1-val)*360. + aoff / np.pi * 180.,
                     horizontalalignment='center', verticalalignment='center')

            if val < 1e0:
                rloff = rloff_list[ii] #0.02
                plt.plot([(rad - size) * np.cos(ang), (1.25 + rloff) * np.cos(ang)],
                         [(rad - size) * np.sin(ang), (1.25 + rloff) * np.sin(ang)], color=colors[ii], alpha=0.8)

                ydate = datetime.datetime.strptime("1/1/70", "%m/%d/%y")
                ydate += datetime.timedelta(days=int(val*365))
                fdate = ydate.strftime('%d %b')

                for uu in range(12):
                    fdate = fdate.replace(months_eng[uu], months[uu])

                plt.text((1.3 + rloff) * np.cos(ang), (1.3 + rloff) * np.sin(ang), fdate, rotation=(1-val) * 360.,
                         horizontalalignment='center', verticalalignment='center', color=colors[ii], alpha=1.)

            wedges_list.append(wedges[0])

        plt.legend(wedges_list,
                   ["ITALIA (ITA)", "EUROPA (EUR)", "CINA (CHN)", "USA", "MONDO (WRD)"],
                   loc="upper right", fontsize=7.5, ncol=1, frameon=False,
                   handletextpad=.4, labelspacing=.1, columnspacing=.2, handlelength=1.)
        #bbox_to_anchor=(0.82, 1.)

        plt.text(0, 0, int(year), horizontalalignment='center', verticalalignment='center', fontsize=16)

        plt.text(1.4, -1.5, "dati: Global Footprint Network", horizontalalignment='right', verticalalignment='bottom', fontsize=6)
        plt.text(-1.5, 1.5, "OVERSHOOT\nDAY", horizontalalignment='left', verticalalignment='top', fontsize=18)

        plt.xlim(-1.5, 1.5)
        plt.ylim(-1.5, 1.5)
        #plt.gca().set_frame_on(True)
        plt.gca().set(aspect="equal")
        plt.tight_layout()
        fname = "plots/plot_%05d.png" % iframe
        plt.savefig(fname)
        plt.close("all")
        iframe += 1

# ending frames
for _ in range(60):
    copyfile(fname, "plots/plot_%05d.png" % iframe)
    iframe += 1



