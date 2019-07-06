import argparse
import json
import svgwrite


class SVG:


    def __init__(self):
        self.dwg = None
        self.BS = 20
        self.BT = 25
        self.IS = 3
        self.LPAD = 20
        self.TPAD = 50
        self.LABELHEIGHT = 10
        self.CL = 10
        self.colors = {'red': 0xe74037, 'orange': 0xe57d1c, 'yellow': 0xf2c73c, 'green': 0x8abc39, 'black': 0x404040, 'blue': 0x1b7192, 'darkgreen': 0x088460}
        for k,v in self.colors.items():
            if k != 'yellow' and k != "black":
                self.colors[k] = self.colors['yellow']
        self.labels = 0

    def start(self, outpath):
        self.dwg = svgwrite.Drawing(outpath)
        self.current_byte = 0
        self.style()
        name = outpath.split(".")[0].replace("_", " 0x").lower()
        self.dwg.add(
            self.dwg.text(f"{name}", insert=(self.LPAD, self.TPAD-self.BS), class_="mainlabel")
        )


    def style(self):
        s = """
            .mainlabel {
                font-size: 8pt;
                font-family: 'Arial';
                font-weight: 700;
            }
            .offsets { 
                font-size: 6pt; 
                font-family: 'Courier New'; 
            }
            .nrbytes { 
                font-size: 6pt; 
                font-family: 'Courier New'; 
                font-style: italic; 
            }
            .bytelabel { 
                font-size: 6pt; 
                font-family: 'Arial'; 
                font-weight: 700;
            }
            .byteoptional { 
                font-size: 6pt; 
                font-family: 'Arial'; 
                font-style: italic;
                font-weight: 300;
            }
            .boxlabel { 
                font-size: 8pt; 
                font-family: 'Arial'; 
                font-weight: 700;
            }
            .boxlabeli { 
                font-size: 8pt; 
                font-family: 'Arial'; 
                font-weight: 700;
                fill: #FFFFFF;
            }
        """
        pattern = self.dwg.pattern(insert=(0,0), size=(4,4), id_="diagonal", patternUnits="userSpaceOnUse")
        path = self.dwg.path(d="M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2", stroke=self.toc(self.colors['black']), stroke_width=1)
        pattern.add(path)
        self.dwg.add(pattern)
        self.dwg.add(
            self.dwg.style(s)
        )

    def save(self):
        self.dwg.save(pretty=True)

    def addbytebox(self, optional=False, size=None, foreground=False, **none):
        if not foreground:
            self.current_byte += 1
            self.labels = 0

        nr = self.current_byte
        offset = (nr -1)*8 * self.BS
        x = offset + self.LPAD


        if not foreground:
            x = offset + self.LPAD
            yy = self.TPAD - 3.5*self.IS
            if optional:
                self.dwg.add(
                    self.dwg.text(f"(optional)", insert=(x, yy), class_="byteoptional")
                )

        if size is None and not foreground:
            self.dwg.add(
                self.dwg.rect((offset + self.LPAD, self.TPAD),
                              size=(8*self.BS, self.BS),
                              fill="white", stroke="black", stroke_width="2")
            )
            for i in range(0,8):
                x = offset + self.LPAD + i*self.BS
                if i > 0:
                    self.dwg.add(
                        self.dwg.line((x, self.TPAD), (x, self.TPAD + self.BS),
                                      stroke="black")
                    )
                self.dwg.add(
                    self.dwg.text(8-i-1, insert=(x + self.BS*0.7, self.TPAD - self.IS), class_="offsets")
                )

        elif not foreground and size:
            self.dwg.add(
                self.dwg.rect((x, self.TPAD),
                              size=(4*self.BS, self.BS),
                              fill="white", stroke="black", stroke_width="2")
            )
            x = offset + self.LPAD
            if type(size) == int:
                sizeinfo = size
            else:
                sizeinfo = ','.join([str(_) for _ in size])
            self.dwg.add(
                self.dwg.text(f"{sizeinfo} bytes", insert=(x + self.IS, self.TPAD - self.IS), class_="nrbytes")
            )
        elif size and foreground:
            t1 = [(0,3),(1,0.5),(-1,-0.5),(0,-3)]
            t2 = [(3,-3),(2,-0.5),(4,0.5),(3,3)]
            t1t = [(x*self.BS/8, y*self.BS/5) for x,y in t1]
            t2t = [(x*self.BS/8, y*self.BS/5) for x,y in t2]
            c = svgwrite.container.Group(transform=f"translate({x + 2*self.BS},{self.TPAD+self.BS/2})")
            c.add(
                self.dwg.polygon(t1t + t2t, stroke="white", stroke_width=1, fill="white")
            )
            c.add(
                self.dwg.polyline(t1t, stroke="black", stroke_width=1, fill="none")
            )
            c.add(
                self.dwg.polyline(t2t, stroke="black", stroke_width=1, fill="none")
            )
            self.dwg.add(c)

    def toc(self, v):
        return "#{:06X}".format(v)

    def addmask(self, f, t, label, color, unused=0, size=None, **tmp):
        if size:
            t = 3
            f = 0
        color = self.colors.get(color, self.colors['green'])
        offset = (self.current_byte -1 )*8 * self.BS
        x = self.LPAD + offset + f*self.BS + self.IS
        y = self.TPAD + self.IS
        w = (t-f+1)*self.BS - self.IS*2
        h = self.BS - self.IS*2

        self.dwg.add(
            self.dwg.rect((x,y), (w,h),
                          fill=self.toc(color), fill_opacity="1", stroke_opacity="0", stroke_width="1")
        )
        if unused:
            w = unused*self.BS - self.IS
            color = self.colors["black"]
            self.dwg.add(
                self.dwg.rect((x,y), (w,h), fill="url(#diagonal)", opacity="0.4" )
            )
        for i in range(f+1,t+1):
            x = offset + self.LPAD + i*self.BS
            continue

            self.dwg.add(
                self.dwg.line((x, self.TPAD+self.IS), (x, self.TPAD + self.BS - self.IS),
                              stroke="white", stroke_width="1", stroke_opacity="0.2")
            )

        if(False and len(label) <= (t+1-f - unused)*2):
            x = self.LPAD + offset + (f + unused)*self.BS + 2*self.IS
            y = self.TPAD + self.BS - 2*self.IS
            self.dwg.add(
                self.dwg.text(label, insert=(x, y), class_="boxlabeli")
            )
        else:
            if size:
                t = 1
            self.labels += 1
            xs = self.LPAD + offset + (f + unused)*self.BS + 0.5*(self.BS*(t-f+1-unused))
            ys = self.TPAD + 0.5*self.BS
            ys2 = self.TPAD + self.BS - self.IS
            xc = xs
            yc = ys + self.labels*self.LABELHEIGHT
            xe = xc + self.CL
            ye = yc + self.CL
            self.dwg.add(
                self.dwg.polyline([(xs, ys2), (xc, yc), (xe, ye)], stroke="white", stroke_width=3, fill="none")
            )
            self.dwg.add(
                self.dwg.polyline([(xs, ys), (xc, yc), (xe, ye)], stroke="black", stroke_width=1, fill="none")
            )
            self.dwg.add(
                self.dwg.circle(center=(xs,ys), r=2)
            )
            self.dwg.add(
                self.dwg.text(label, insert=(xe + self.IS, ye + self.IS),class_="boxlabel")
            )
        self.dwg.save()


class Visualizer:

    def __init__(self, path):
        self.data = self.load(path)
        self.svg = SVG()

    def fromto(self, mask):
        mask = int(mask, 16)
        f = None
        t = None
        for i in range(8):
            check = (1 << (7-i))
            if check & mask:
                if t:
                    raise ValueError("mask %s has multiple regions", hex(mask))
                if f is None:
                    f = i
            else:
                if f is not None and t is None:
                    t = i - 1
        if t is None:
            t = 7
        return f, t



    def draw(self):
        for instr, infos in self.data.items():
            self.svg.start(f"{instr}.svg")
            for b in infos['bytes']:
                self.svg.addbytebox(**b)
                for boxlabel, boxinfo in sorted(b['labels'].items(), key=lambda x: int(x[1]['used'],16)):
                    f, t = self.fromto(boxinfo['used'])
                    color = boxinfo.get('color')
                    unused = boxinfo.get('unused', 0)
                    self.svg.addmask(f, t, boxlabel, color, unused, **b)
                self.svg.addbytebox(foreground=True, **b)

            self.svg.save()

    @staticmethod
    def load(path):
        print(f"loading {path}")
        with open(path, 'r') as r:
            return json.load(r)


def do(path):
    v = Visualizer(path)
    v.draw()

    with open(path, 'r') as r:
        data = json.load(r)

    for instr, infos in data.items():
        opcodes = sorted(infos['opcodes'])
        oc = opcodes[0]
        print("\n### {}".format("Instruction 0x{:02X}".format(oc)))
        print("| {} | {} | {} |".format("field", "length (bits)", "description"))
        print("| --- | --- | --- |")

        for i,b in enumerate(infos['bytes']):
            sizel = b.get('size', None)
            for boxlabel, boxinfo in sorted(b['labels'].items(), key=lambda x: int(x[1]['used'],16), reverse=True):
                f, t = v.fromto(boxinfo['used'])
                f = 8 - f - 1
                t = 8 - t - 1
                if not sizel:
                    size = f -t + 1
                else:
                    if type(sizel) == int:
                        size = sizel*8
                    else:
                        size = ", ".join([str(_*8) for _ in sizel[:-1]])
                        size += " or " + str(sizel[-1]*8)

                desc = ""
                if boxlabel == "opcode":
                    desc += "must be "
                    if len(opcodes) > 1:
                        desc += ", ".join(["0x{:02X}".format(_) for _ in opcodes[:-1]])
                    else:
                        desc += ", ".join(["0x{:02X}".format(_) for _ in opcodes])
                    if len(opcodes) > 1:
                        desc += " or " + "0x{:02X}".format(opcodes[-1])
                print("| {} | {} | {} |".format(boxlabel, size, desc))


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data")
    args = parser.parse_args()
    do(args.data)
