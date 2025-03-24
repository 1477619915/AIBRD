import os
import xml.etree.ElementTree as ElementTree
import csv

single_csvfile = open("single.csv", "w", encoding="UTF-8", newline='')
single_writer = csv.writer(single_csvfile)
single_writer.writerow(["sentence", "ob", "eb", "sr", "pattern"])

multi_csvfile = open("multi.csv", "w", encoding="UTF-8", newline='')
multi_writer = csv.writer(multi_csvfile)
multi_writer.writerow(["sentence", "ob", "eb", "sr", "patterns"])


def extractSentence(fileName):
    tree = ElementTree.ElementTree(file=fileName)
    root = tree.getroot()
    single = 0
    multi = 0

    for tag in root:
        if len(tag.attrib) > 0:
            if tag.attrib["ob"] == "" and tag.attrib["eb"] == "" and tag.attrib["sr"] == "":
                if "patterns" in tag.attrib:
                    single_writer.writerow([tag.text, 0, 0, 0, tag.attrib["patterns"]])
                else:
                    single_writer.writerow([tag.text, 0, 0, 0, ""])
                single += 1
            elif tag.attrib["ob"] == "x" and tag.attrib["eb"] == "" and tag.attrib["sr"] == "":
                if "patterns" in tag.attrib:
                    single_writer.writerow([tag.text, 1, 0, 0, tag.attrib["patterns"]])
                else:
                    single_writer.writerow([tag.text, 1, 0, 0, ""])
                single += 1
            elif tag.attrib["ob"] == "" and tag.attrib["eb"] == "x" and tag.attrib["sr"] == "":
                if "patterns" in tag.attrib:
                    single_writer.writerow([tag.text, 0, 1, 0, tag.attrib["patterns"]])
                else:
                    single_writer.writerow([tag.text, 0, 1, 0, ""])
                single += 1
            elif tag.attrib["ob"] == "" and tag.attrib["eb"] == "" and tag.attrib["sr"] == "x":
                if "patterns" in tag.attrib:
                    single_writer.writerow([tag.text, 0, 0, 1, tag.attrib["patterns"]])
                else:
                    single_writer.writerow([tag.text, 0, 0, 1, ""])
                single += 1
            elif tag.attrib["ob"] == "x" and tag.attrib["eb"] == "x" and tag.attrib["sr"] == "":
                if "patterns" in tag.attrib:
                    multi_writer.writerow([tag.text, 1, 1, 0, tag.attrib["patterns"]])
                else:
                    multi_writer.writerow([tag.text, 1, 1, 0, ""])
                multi += 1
            elif tag.attrib["ob"] == "x" and tag.attrib["eb"] == "" and tag.attrib["sr"] == "x":
                if "patterns" in tag.attrib:
                    multi_writer.writerow([tag.text, 1, 0, 1, tag.attrib["patterns"]])
                else:
                    multi_writer.writerow([tag.text, 1, 0, 1, ""])
                multi += 1
            elif tag.attrib["ob"] == "" and tag.attrib["eb"] == "x" and tag.attrib["sr"] == "x":
                if "patterns" in tag.attrib:
                    multi_writer.writerow([tag.text, 0, 1, 1, tag.attrib["patterns"]])
                else:
                    multi_writer.writerow([tag.text, 0, 1, 1, ""])
                multi += 1
            elif tag.attrib["ob"] == "x" and tag.attrib["eb"] == "x" and tag.attrib["sr"] == "x":
                if "patterns" in tag.attrib:
                    multi_writer.writerow([tag.text, 1, 1, 1, tag.attrib["patterns"]])
                else:
                    multi_writer.writerow([tag.text, 1, 1, 1, ""])
                multi += 1

        if len(tag.tag) > 0:
            for a_tag in tag:
                for b_tag in a_tag:
                    if b_tag.attrib["ob"] == "" and b_tag.attrib["eb"] == "" and b_tag.attrib["sr"] == "":
                        if "patterns" in b_tag.attrib:
                            single_writer.writerow([b_tag.text, 0, 0, 0, b_tag.attrib["patterns"]])
                        else:
                            single_writer.writerow([b_tag.text, 0, 0, 0, ""])
                        single += 1
                    elif b_tag.attrib["ob"] == "x" and b_tag.attrib["eb"] == "" and b_tag.attrib["sr"] == "":
                        if "patterns" in b_tag.attrib:
                            single_writer.writerow([b_tag.text, 1, 0, 0, b_tag.attrib["patterns"]])
                        else:
                            single_writer.writerow([b_tag.text, 1, 0, 0, ""])
                        single += 1
                    elif b_tag.attrib["ob"] == "" and b_tag.attrib["eb"] == "x" and b_tag.attrib["sr"] == "":
                        if "patterns" in b_tag.attrib:
                            single_writer.writerow([b_tag.text, 0, 1, 0, b_tag.attrib["patterns"]])
                        else:
                            single_writer.writerow([b_tag.text, 0, 1, 0, ""])
                        single += 1
                    elif b_tag.attrib["ob"] == "" and b_tag.attrib["eb"] == "" and b_tag.attrib["sr"] == "x":
                        if "patterns" in b_tag.attrib:
                            single_writer.writerow([b_tag.text, 0, 0, 1, b_tag.attrib["patterns"]])
                        else:
                            single_writer.writerow([b_tag.text, 0, 0, 1, ""])
                        single += 1
                    elif b_tag.attrib["ob"] == "x" and b_tag.attrib["eb"] == "x" and b_tag.attrib["sr"] == "":
                        if "patterns" in b_tag.attrib:
                            multi_writer.writerow([b_tag.text, 1, 1, 0, b_tag.attrib["patterns"]])
                        else:
                            multi_writer.writerow([b_tag.text, 1, 1, 0, ""])
                        multi += 1
                    elif b_tag.attrib["ob"] == "x" and b_tag.attrib["eb"] == "" and b_tag.attrib["sr"] == "x":
                        if "patterns" in b_tag.attrib:
                            multi_writer.writerow([b_tag.text, 1, 0, 1, b_tag.attrib["patterns"]])
                        else:
                            multi_writer.writerow([b_tag.text, 1, 0, 1, ""])
                        multi += 1
                    elif b_tag.attrib["ob"] == "" and b_tag.attrib["eb"] == "x" and b_tag.attrib["sr"] == "x":
                        if "patterns" in b_tag.attrib:
                            multi_writer.writerow([b_tag.text, 0, 1, 1, b_tag.attrib["patterns"]])
                        else:
                            multi_writer.writerow([b_tag.text, 0, 1, 1, ""])
                        multi += 1
                    elif b_tag.attrib["ob"] == "x" and b_tag.attrib["eb"] == "x" and b_tag.attrib["sr"] == "x":
                        if "patterns" in b_tag.attrib:
                            multi_writer.writerow([b_tag.text, 1, 1, 1, b_tag.attrib["patterns"]])
                        else:
                            multi_writer.writerow([b_tag.text, 1, 1, 1, ""])
                        multi += 1
    return (single, multi)


single = 0
multi = 0
for filepath, dirnames, filenames in os.walk(r'D:\桌面\issue\pratice\python\sentenClassfication\1_pattern_labeled_data'):
    for filename in filenames:
        num1, num2 = extractSentence(filepath + "\\" + filename)
        single = single + num1
        multi = multi + num2

print(single)
print(multi)

single_csvfile.close()
multi_csvfile.close()