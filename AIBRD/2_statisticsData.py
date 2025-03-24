import os
import xml.etree.ElementTree as ElementTree
import csv


statistic_csvfile = open("statistic.csv", "w", encoding="UTF-8", newline='')
statistic_writer = csv.writer(statistic_csvfile)
statistic_writer.writerow(["project", "id", "sentence", "patterns", "ob", "eb", "sr"])


def statistics_data(projectname, filename):
    tree = ElementTree.ElementTree(file=filename)
    root = tree.getroot()
    id = root.find('id').text

    # 获取title节点写入csv文件
    for title in root.findall('title'):
        if title.attrib["ob"] == "" and title.attrib["eb"] == "" and title.attrib["sr"] == "":
            if "patterns" in title.attrib:
                statistic_writer.writerow([projectname, id, title.text, title.attrib["patterns"], 0, 0, 0])
            else:
                statistic_writer.writerow([projectname, id, title.text, "", 0, 0, 0])
        elif title.attrib["ob"] == "x" and title.attrib["eb"] == "" and title.attrib["sr"] == "":
            if "patterns" in title.attrib:
                statistic_writer.writerow([projectname, id, title.text, title.attrib["patterns"], 1, 0, 0])
            else:
                statistic_writer.writerow([projectname, id, title.text, "", 1, 0, 0])
        elif title.attrib["ob"] == "" and title.attrib["eb"] == "x" and title.attrib["sr"] == "":
            if "patterns" in title.attrib:
                statistic_writer.writerow([projectname, id, title.text, title.attrib["patterns"], 0, 1, 0])
            else:
                statistic_writer.writerow([projectname, id, title.text, "", 0, 1, 0])
        elif title.attrib["ob"] == "" and title.attrib["eb"] == "" and title.attrib["sr"] == "x":
            if "patterns" in title.attrib:
                statistic_writer.writerow([projectname, id, title.text, title.attrib["patterns"], 0, 0, 1])
            else:
                statistic_writer.writerow([projectname, id, title.text, "", 0, 0, 1])
        elif title.attrib["ob"] == "x" and title.attrib["eb"] == "x" and title.attrib["sr"] == "":
            if "patterns" in title.attrib:
                statistic_writer.writerow([projectname, id, title.text, title.attrib["patterns"], 1, 1, 0])
            else:
                statistic_writer.writerow([projectname, id, title.text, "", 1, 1, 0])
        elif title.attrib["ob"] == "x" and title.attrib["eb"] == "" and title.attrib["sr"] == "x":
            if "patterns" in title.attrib:
                statistic_writer.writerow([projectname, id, title.text, title.attrib["patterns"], 1, 0, 1])
            else:
                statistic_writer.writerow([projectname, id, title.text, "", 1, 0, 1])
        elif title.attrib["ob"] == "" and title.attrib["eb"] == "x" and title.attrib["sr"] == "x":
            if "patterns" in title.attrib:
                statistic_writer.writerow([projectname, id, title.text, title.attrib["patterns"], 0, 1, 1])
            else:
                statistic_writer.writerow([projectname, id, title.text, "", 0, 1, 1])
        elif title.attrib["ob"] == "x" and title.attrib["eb"] == "x" and title.attrib["sr"] == "x":
            if "patterns" in title.attrib:
                statistic_writer.writerow([projectname, id, title.text, title.attrib["patterns"], 1, 1, 1])
            else:
                statistic_writer.writerow([projectname, id, title.text, "", 1, 1, 1])

    # 获取desc.parg.st，根据属性写入csv文件
    for desc in root.findall('desc'):
        for parg in desc.findall('parg'):
            if parg.attrib["ob"] == "x" or parg.attrib["eb"] == "x" or parg.attrib["sr"] == "x":
                parg_ob = 0 if parg.attrib["ob"] == "" else 1
                parg_eb = 0 if parg.attrib["eb"] == "" else 1
                parg_sr = 0 if parg.attrib["sr"] == "" else 1
                parg_patterns = "" if "patterns" not in parg.attrib else parg.attrib["patterns"]

                for sentence in parg.findall('st'):
                    if sentence.attrib["ob"] == "" and sentence.attrib["eb"] == "" and sentence.attrib["sr"] == "":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"] + "," + parg_patterns, parg_ob, parg_eb, parg_sr])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, parg_patterns, parg_ob, parg_eb, parg_sr])
                    elif sentence.attrib["ob"] == "x" and sentence.attrib["eb"] == "" and sentence.attrib["sr"] == "":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"] + "," + parg_patterns, 1, parg_eb, parg_sr])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, parg_patterns, 1, parg_eb, parg_sr])
                    elif sentence.attrib["ob"] == "" and sentence.attrib["eb"] == "x" and sentence.attrib["sr"] == "":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"] + "," + parg_patterns, parg_ob, 1, parg_sr])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, parg_patterns, parg_ob, 1, parg_sr])
                    elif sentence.attrib["ob"] == "" and sentence.attrib["eb"] == "" and sentence.attrib["sr"] == "x":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"] + "," + parg_patterns, parg_ob, parg_eb, 1])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, parg_patterns, parg_ob, parg_eb, 1])
                    elif sentence.attrib["ob"] == "x" and sentence.attrib["eb"] == "x" and sentence.attrib["sr"] == "":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"] + "," + parg_patterns, 1, 1, parg_sr])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, parg_patterns, 1, 1, parg_sr])
                    elif sentence.attrib["ob"] == "x" and sentence.attrib["eb"] == "" and sentence.attrib["sr"] == "x":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"] + "," + parg_patterns, 1, parg_eb, 1])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, parg_patterns, 1, parg_eb, 1])
                    elif sentence.attrib["ob"] == "" and sentence.attrib["eb"] == "x" and sentence.attrib["sr"] == "x":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"] + "," + parg_patterns, parg_ob, 1, 1])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, parg_patterns, parg_ob, 1, 1])
                    elif sentence.attrib["ob"] == "x" and sentence.attrib["eb"] == "x" and sentence.attrib["sr"] == "x":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"] + "," + parg_patterns, 1, 1, 1])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, parg_patterns, 1, 1, 1])
            else:
                for sentence in parg.findall('st'):
                    if sentence.attrib["ob"] == "" and sentence.attrib["eb"] == "" and sentence.attrib["sr"] == "":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"], 0, 0, 0])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, "", 0, 0, 0])
                    elif sentence.attrib["ob"] == "x" and sentence.attrib["eb"] == "" and sentence.attrib["sr"] == "":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"], 1, 0, 0])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, "", 1, 0, 0])
                    elif sentence.attrib["ob"] == "" and sentence.attrib["eb"] == "x" and sentence.attrib["sr"] == "":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"], 0, 1, 0])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, "", 0, 1, 0])
                    elif sentence.attrib["ob"] == "" and sentence.attrib["eb"] == "" and sentence.attrib["sr"] == "x":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"], 0, 0, 1])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, "", 0, 0, 1])
                    elif sentence.attrib["ob"] == "x" and sentence.attrib["eb"] == "x" and sentence.attrib["sr"] == "":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"], 1, 1, 0])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, "", 1, 1, 0])
                    elif sentence.attrib["ob"] == "x" and sentence.attrib["eb"] == "" and sentence.attrib["sr"] == "x":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"], 1, 0, 1])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, "", 1, 0, 1])
                    elif sentence.attrib["ob"] == "" and sentence.attrib["eb"] == "x" and sentence.attrib["sr"] == "x":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"], 0, 1, 1])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, "", 0, 1, 1])
                    elif sentence.attrib["ob"] == "x" and sentence.attrib["eb"] == "x" and sentence.attrib["sr"] == "x":
                        if "patterns" in sentence.attrib:
                            statistic_writer.writerow([projectname, id, sentence.text, sentence.attrib["patterns"], 1, 1, 1])
                        else:
                            statistic_writer.writerow([projectname, id, sentence.text, "", 1, 1, 1])


for filepath, dirnames, filenames in os.walk(r'D:\桌面\issue\pratice\python\sentenClassfication\1_pattern_labeled_data'):
    for filename in filenames:
        statistics_data(filepath.split('\\')[-1], filepath + "\\" + filename)
