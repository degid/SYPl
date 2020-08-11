
class ImageTypeError(Exception):
    def __str__(self):
        return 'The image must be in Px PPM'


class ImageReadError(Exception):
    def __str__(self):
        return 'Invalid character in tag'


def getNumsPPM():
    PPMnums = []
    PPMnums.append(b'\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8Mp\xcfr\x8d\xd5\x8f\x83\xd3\x85R\xc9VI\xc8MI\xc8M\x00I\xc8MI\xc8M\xa2\xdb\xa3\xf9\xfc\xf9\xec\xf7\xec\xf4\xfa\xf5\xd8\xee\xd8V\xcaYI\xc8M\x00I\xc8M]\xcb`\xf0\xf8\xf0\xac\xdf\xadK\xc8Of\xcdh\xef\xf8\xef\xa6\xdd\xa7I\xc8M\x00I\xc8M\x94\xd7\x96\xf4\xfa\xf5]\xcb`I\xc8MK\xc8O\xc8\xe8\xc9\xd5\xed\xd5O\xc9R\x00I\xc8M\xae\xdf\xaf\xe8\xf5\xe8V\xcaYI\xc8MI\xc8M\xb4\xe1\xb5\xe5\xf4\xe5T\xcaW\x00I\xc8M\xb6\xe2\xb7\xe4\xf3\xe4T\xcaWI\xc8MI\xc8M\xae\xdf\xaf\xea\xf6\xeaV\xcaY\x00I\xc8M\xb5\xe1\xb6\xe6\xf4\xe6V\xcaYI\xc8MI\xc8M\xb0\xe0\xb1\xe9\xf5\xe9V\xcaY\x00I\xc8M\xa6\xdd\xa7\xee\xf8\xeeY\xca\\I\xc8MI\xc8M\xbc\xe4\xbd\xe0\xf2\xe0R\xc9V\x00I\xc8M{\xd1}\xf7\xfc\xf8~\xd2\x80I\xc8MQ\xc9T\xd9\xef\xd9\xc4\xe7\xc4K\xc8O\x00I\xc8MO\xc9R\xd5\xed\xd5\xe1\xf2\xe1s\xcfu\xb8\xe2\xb8\xf6\xfb\xf6{\xd1}I\xc8M\x00I\xc8MI\xc8M`\xccc\xcc\xea\xcd\xfa\xfd\xfa\xe8\xf5\xe8\x8c\xd5\x8eK\xc8OI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00')
    PPMnums.append(b'\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8M\\\xcb_\x8d\xd5\x8fQ\xc9TI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8M\x86\xd4\x88\xf8\xfc\xf8f\xcdhI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8M\x86\xd4\x88\xf8\xfc\xf8f\xcdhI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8M\x86\xd4\x88\xf8\xfc\xf8f\xcdhI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8M\x86\xd4\x88\xf8\xfc\xf8f\xcdhI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8M\x86\xd4\x88\xf8\xfc\xf8f\xcdhI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8M\x86\xd4\x88\xf8\xfc\xf8f\xcdhI\xc8MI\xc8M\x00I\xc8MK\xc8O\xa9\xdd\xaa\x8a\xd5\x8b\x88\xd4\x89\xf8\xfc\xf8f\xcdhI\xc8MI\xc8M\x00I\xc8MI\xc8M\x92\xd7\x93\xf4\xfa\xf4\xea\xf6\xea\xfa\xfd\xfaf\xcdhI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8Mh\xcdk\xe3\xf3\xe3\xfb\xfd\xfbf\xcdhI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8Mk\xcem\xee\xf7\xeef\xcdhI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00')
    PPMnums.append(b'\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00I\xc8My\xd0{\x91\xd6\x92\x91\xd6\x92\x91\xd6\x92\x91\xd6\x92\x91\xd6\x92\x85\xd3\x87K\xc8O\x00I\xc8M\xb8\xe2\xb8\xfe\xff\xfe\xf2\xf9\xf2\xef\xf8\xef\xef\xf8\xef\xef\xf8\xef\xd7\xee\xd8R\xc9V\x00I\xc8Mb\xccd\xee\xf8\xee\xcd\xea\xceV\xcaYM\xc9QM\xc9QK\xc8OI\xc8M\x00I\xc8MI\xc8M~\xd2\x80\xf4\xfa\xf4\xce\xea\xceW\xcaZI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8Mu\xcfw\xef\xf8\xef\xd8\xee\xd8Y\xca\\I\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8Mk\xcem\xec\xf7\xec\xd6\xed\xd6T\xcaWI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8Mv\xd0x\xf5\xfb\xf5\xac\xdf\xadI\xc8M\x00I\xc8MO\xc9RY\xca\\I\xc8MI\xc8MK\xc8O\xc7\xe8\xc7\xdc\xf0\xdcR\xc9V\x00I\xc8M\x9b\xd9\x9c\xf3\xfa\xf3_\xcbbI\xc8MK\xc8O\xc2\xe6\xc3\xde\xf1\xdeR\xc9V\x00I\xc8M]\xcb`\xed\xf7\xed\xd5\xed\xd6l\xceo\xa1\xdb\xa2\xf7\xfb\xf7\xae\xdf\xafI\xc8M\x00I\xc8MI\xc8Ms\xcfu\xd6\xee\xd7\xfa\xfd\xfa\xf0\xf8\xf0\xa9\xdd\xaaM\xc9QI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00')
    PPMnums.append(b'\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MK\xc8Ox\xd0z\x8e\xd6\x90\x83\xd3\x85T\xcaWI\xc8MI\xc8M\x00I\xc8MM\xc9Q\xc0\xe5\xc0\xf8\xfc\xf8\xec\xf6\xec\xf3\xfa\xf3\xe6\xf4\xe7f\xcdhI\xc8M\x00I\xc8M\x88\xd4\x89\xf8\xfc\xf8\x92\xd7\x93K\xc8OZ\xcb]\xe4\xf3\xe4\xcd\xea\xceM\xc9Q\x00I\xc8M\x99\xd9\x9a\xd2\xec\xd2T\xcaWI\xc8MI\xc8M\xb3\xe1\xb4\xec\xf6\xecW\xcaZ\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MK\xc8O\xc1\xe6\xc2\xe6\xf4\xe6T\xcaW\x00I\xc8MI\xc8MI\xc8MV\xcaYz\xd1|\xb0\xe0\xb1\xf8\xfc\xf8\xad\xdf\xaeI\xc8M\x00I\xc8MI\xc8MI\xc8M\\\xcb_\xf4\xfa\xf4\xfc\xfe\xfc\xbc\xe4\xbdO\xc9RI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MO\xc9R\x82\xd3\x84\xf5\xfb\xf5\x95\xd8\x96I\xc8M\x00I\xc8M\x80\xd2\x82\xd5\xed\xd6Z\xcb]I\xc8MW\xcaZ\xe9\xf5\xe9\xb0\xe0\xb1I\xc8M\x00I\xc8Mc\xccf\xf1\xf9\xf1\xcf\xeb\xd0o\xceq\xba\xe3\xbb\xf7\xfb\xf7{\xd1}I\xc8M\x00I\xc8MI\xc8My\xd0{\xdc\xf0\xdd\xfb\xfd\xfb\xe3\xf3\xe3\x88\xd4\x89K\xc8OI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00')
    PPMnums.append(b'\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MK\xc8O|\xd1~w\xd0yI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MO\xc9R\xd3\xec\xd3\xc7\xe8\xc8K\xc8OI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MM\xc9Q\xd2\xec\xd2\xc7\xe8\xc8I\xc8MI\xc8M\x00V\xcaY\xe5\xf4\xe5\xfa\xfd\xfa\xfa\xfd\xfa\xfa\xfd\xfa\xfd\xfe\xfd\xfd\xfe\xfd\xe8\xf5\xe9V\xcaY\x00O\xc9R\xd2\xec\xd2\xca\xe9\xcbf\xcdhg\xcdj\xd6\xed\xd6\xcc\xea\xcc`\xcccI\xc8M\x00I\xc8Mj\xcdl\xf0\xf8\xf0\x8c\xd5\x8eO\xc9R\xd3\xec\xd3\xc7\xe8\xc8K\xc8OI\xc8M\x00I\xc8MI\xc8M\xa6\xdd\xa7\xe6\xf4\xe6]\xcb`\xd3\xec\xd3\xc7\xe8\xc8K\xc8OI\xc8M\x00I\xc8MI\xc8MQ\xc9T\xd4\xed\xd5\xc0\xe5\xc1\xd3\xec\xd4\xc7\xe8\xc8K\xc8OI\xc8M\x00I\xc8MI\xc8MI\xc8Mn\xcep\xf0\xf8\xf0\xea\xf6\xea\xc7\xe8\xc8K\xc8OI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8M\xa7\xdd\xa8\xfd\xfe\xfd\xc7\xe8\xc8K\xc8OI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MQ\xc9T\xd6\xee\xd7\xc7\xe8\xc7K\xc8OI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00')
    PPMnums.append(b'\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8Mw\xd0y\x8e\xd6\x90\x82\xd3\x84T\xcaWI\xc8MI\xc8M\x00I\xc8MM\xc9Q\xbd\xe4\xbe\xf9\xfc\xf9\xec\xf6\xec\xf4\xfa\xf4\xe2\xf2\xe2`\xcccI\xc8M\x00I\xc8M\x83\xd3\x85\xf9\xfc\xf9\x9c\xd9\x9dK\xc8O]\xcb`\xe7\xf5\xe8\xc5\xe7\xc6K\xc8O\x00I\xc8M\xa9\xdd\xaa\xe2\xf2\xe2W\xcaZI\xc8MI\xc8M\xb1\xe0\xb2\xec\xf7\xedW\xcaZ\x00I\xc8MI\xc8MM\xc9QI\xc8MI\xc8MI\xc8M\xa4\xdc\xa5\xf4\xfa\xf4Z\xcb]\x00I\xc8MQ\xc9Tf\xcdhO\xc9RI\xc8MK\xc8O\xc3\xe6\xc4\xe6\xf4\xe7V\xcaY\x00I\xc8M{\xd1}\xfa\xfd\xfa\xd6\xed\xd6z\xd1|\xb4\xe1\xb5\xf9\xfc\xf9\xaa\xde\xaaI\xc8M\x00I\xc8MZ\xcb]\xf1\xf9\xf1\xc8\xe8\xc9\xee\xf8\xee\xec\xf6\xec\x9c\xd9\x9dM\xc9QI\xc8M\x00I\xc8MR\xc9V\xde\xf1\xde\xb3\xe1\xb4I\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00I\xc8MK\xc8O\xc8\xe8\xc8\xd9\xef\xda\x8e\xd6\x90\x8d\xd5\x8f\x8d\xd5\x8fr\xcftI\xc8M\x00I\xc8MI\xc8M\xac\xde\xad\xfd\xfe\xfd\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc3\xe6\xc4I\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00')
    PPMnums.append(b'\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8Mj\xcdl\x8c\xd5\x8e\x86\xd4\x88Y\xca\\I\xc8MI\xc8M\x00I\xc8MK\xc8O\x9e\xda\x9f\xf8\xfc\xf8\xed\xf7\xed\xf1\xf9\xf2\xe9\xf5\xe9g\xcdjI\xc8M\x00I\xc8Mc\xccf\xf4\xfa\xf4\xae\xdf\xafM\xc9QW\xcaZ\xdf\xf1\xe0\xc8\xe8\xc9K\xc8O\x00I\xc8M\xa2\xdb\xa3\xf4\xfa\xf4\\\xcb_I\xc8MI\xc8M\xb0\xe0\xb1\xe7\xf5\xe8V\xcaY\x00I\xc8M\xb9\xe3\xba\xf2\xf9\xf2Z\xcb]I\xc8MI\xc8M\xaf\xdf\xb0\xea\xf6\xeaV\xcaY\x00I\xc8M\xbf\xe5\xc0\xfd\xfe\xfd\xa8\xdd\xa9O\xc9R]\xcb`\xe0\xf2\xe1\xce\xea\xceM\xc9Q\x00I\xc8M\xb9\xe3\xba\xe3\xf3\xe3\xe9\xf5\xe9\xf4\xfa\xf4\xf7\xfb\xf7\xeb\xf6\xebj\xcdlI\xc8M\x00I\xc8M\xa5\xdc\xa6\xe6\xf4\xe6_\xcbbr\xcfts\xcfuV\xcaYI\xc8MI\xc8M\x00I\xc8Mr\xcft\xf6\xfb\xf6\x84\xd3\x86I\xc8MK\xc8O\xb8\xe2\xb8\xbf\xe5\xc0O\xc9R\x00I\xc8MM\xc9Q\xcc\xea\xcd\xeb\xf6\xeb\x83\xd3\x85\x9e\xda\x9f\xf6\xfb\xf6\xad\xdf\xaeI\xc8M\x00I\xc8MI\xc8MW\xcaZ\xba\xe3\xbb\xf5\xfb\xf5\xf4\xfa\xf4\xb1\xe0\xb2O\xc9RI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00')
    PPMnums.append(b'\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MM\xc9Q\x8d\xd5\x8fb\xccdI\xc8MI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MY\xca\\\xf2\xf9\xf2\xa3\xdc\xa4I\xc8MI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MT\xcaW\xe4\xf3\xe4\xba\xe3\xbbI\xc8MI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MM\xc9Q\xcc\xea\xcc\xd7\xee\xd8Q\xc9TI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8M\xa2\xdb\xa3\xf5\xfb\xf5c\xccfI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8Mb\xccd\xf4\xfa\xf4\xa9\xdd\xaaI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MK\xc8O\xc7\xe8\xc7\xe4\xf3\xe4V\xcaYI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8Ms\xcfu\xf6\xfb\xf6\x9e\xda\x9fI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MK\xc8O\xbe\xe5\xbe\xea\xf6\xeaZ\xcb]I\xc8M\x00I\xc8Mh\xcdk\x8c\xd5\x8e\x8d\xd5\x8f\x8d\xd5\x8f\x95\xd8\x96\xed\xf7\xed\xc9\xe9\xc9M\xc9Q\x00I\xc8M\xac\xdf\xad\xfe\xfe\xfe\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf0\xf8\xf0W\xcaZ\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00')
    PPMnums.append(b'\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8Mw\xd0y\x8e\xd6\x90\x87\xd4\x89Z\xcb]I\xc8MI\xc8M\x00I\xc8MM\xc9Q\xc2\xe6\xc2\xf8\xfc\xf8\xec\xf6\xec\xf1\xf9\xf1\xef\xf8\xefs\xcfuI\xc8M\x00I\xc8M\x90\xd6\x91\xf8\xfc\xf8\x8c\xd5\x8dK\xc8OT\xcaW\xd6\xee\xd7\xd6\xee\xd7Q\xc9T\x00I\xc8M\xb6\xe2\xb7\xe6\xf4\xe6T\xcaWI\xc8MI\xc8M\xa6\xdd\xa7\xed\xf7\xeeW\xcaZ\x00I\xc8M\xa9\xdd\xaa\xef\xf8\xef_\xcbbI\xc8MK\xc8O\xbc\xe4\xbd\xe4\xf3\xe4T\xcaW\x00I\xc8M\\\xcb_\xe7\xf5\xe7\xdd\xf0\xdd\x80\xd2\x82\xb2\xe0\xb3\xf6\xfb\xf6\x9c\xda\x9dI\xc8M\x00I\xc8MI\xc8M\x88\xd4\x89\xf2\xf9\xf2\xf9\xfc\xf9\xfa\xfd\xfa\xc7\xe8\xc8R\xc9VI\xc8M\x00I\xc8MW\xcaZ\xee\xf7\xee\xb7\xe2\xb8Q\xc9To\xceq\xf1\xf9\xf1\xaa\xde\xaaI\xc8M\x00I\xc8Mg\xcdj\xf8\xfc\xf8\x8f\xd6\x91I\xc8MT\xcaW\xe1\xf2\xe2\xbf\xe5\xc0I\xc8M\x00I\xc8MR\xc9V\xe1\xf2\xe1\xe1\xf2\xe1w\xd0y\xb4\xe1\xb4\xf9\xfc\xf9\x8d\xd5\x8fI\xc8M\x00I\xc8MI\xc8Mj\xcdl\xd3\xec\xd3\xfa\xfd\xfa\xec\xf7\xec\x98\xd8\x9aK\xc8OI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00')
    PPMnums.append(b'\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00I\xc8MI\xc8MM\xc9Q~\xd2\x80\x8e\xd6\x90{\xd1}K\xc8OI\xc8MI\xc8M\x00I\xc8MO\xc9R\xcb\xe9\xcc\xf7\xfb\xf7\xeb\xf6\xeb\xf6\xfb\xf6\xcc\xea\xccQ\xc9TI\xc8M\x00I\xc8M}\xd1\x7f\xf6\xfb\xf6\x82\xd3\x84K\xc8On\xcep\xf1\xf9\xf2\xa2\xdb\xa3I\xc8M\x00I\xc8MM\xc9QY\xca\\I\xc8MI\xc8MK\xc8O\xc5\xe7\xc5\xd5\xed\xd5O\xc9R\x00I\xc8MI\xc8Mj\xcdl\xd4\xed\xd5\xf2\xf9\xf2\xc5\xe7\xc5\xae\xdf\xaf\xe7\xf5\xe7V\xcaY\x00I\xc8M]\xcb`\xec\xf7\xed\xe0\xf2\xe0\x81\xd2\x83\xb6\xe2\xb7\xf5\xfa\xf5\xf0\xf8\xf0W\xcaZ\x00I\xc8M\xa4\xdc\xa5\xf3\xfa\xf3b\xccdI\xc8MM\xc9Q\xcd\xea\xcd\xf1\xf9\xf1W\xcaZ\x00I\xc8M\xb6\xe2\xb7\xe5\xf4\xe5T\xcaWI\xc8MI\xc8M\xb6\xe2\xb6\xe8\xf5\xe8V\xcaY\x00I\xc8M\xa4\xdc\xa5\xf5\xfa\xf5e\xccgI\xc8MM\xc9Q\xcb\xe9\xcc\xcf\xeb\xd0M\xc9Q\x00I\xc8M_\xcbb\xec\xf7\xec\xdf\xf1\xe0u\xcfw\xad\xdf\xae\xf5\xfa\xf5\x81\xd2\x83I\xc8M\x00I\xc8MI\xc8Mp\xcfr\xd6\xee\xd7\xfa\xfd\xfa\xe4\xf3\xe4\x85\xd3\x87I\xc8MI\xc8M\x00I\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8MI\xc8M\x00')
    return PPMnums
