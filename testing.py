from pandas import isna


def test_ochra(ochra, dataset, check_info='@$%&'):
    ''' Checks whether OCHRA information is in the excepted format.

    Parameters
    ----------
    ochra : 2D ndarray
        Numpy array representing the OCHRA information, as labelled using the
        ochra.label_ochra function.
    dataset : str
        Specifies whether the OCHRA information comes from 2D3D or ALACART.
    check_info : str, optional
        String that will be checked for in the 'Further info' column. If the
        passed string is found in an instance, an Exception is raised. The
        default is '@$%&'.

    Raises
    ------
    ValueError
        Selected dataset must be be either 2D3D or ALACART.
    Exception
        Found <check_info> in Further Info.

    Returns
    -------
    None.

    '''

    dataset = dataset.lower()
    if dataset not in ['alacart', '2d3d']:
        raise ValueError("Selected dataset must be be either 2D3D or ALACART.")

    ## Noting down the column numbers of each of event
    task, subtask, label, timecode, subfile, errors = 0, 1, 2, 3, 4, 5
    conseq, eem, instr, severity, loc, info = 6, 7, 8, 9, 10, 11

    ## Setting variables for the checks
    if dataset == '2d3d':
        # 'Task Area' tests. Confirming all instances are between 2-10
        area_nums = list(range(2, 11))
        # 'Subtask Area' tests. Confirming all instances are between a-d
        sub_area_letters = ['a', 'b', 'c', 'd']
        # 'Subfile' tests. Confirming all instances are between 1-11 (1st
        # character in most cases) & A-Z (2nd charecter in most cases)
        vid_nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                    '26', '27']
        vid_letters = ['AA', 'AB', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                       'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                       'U', 'V', 'W', 'X', 'Y', 'Z']
    elif dataset == 'alacart':
        area_nums = list(range(6, 11))  # Confirming all instances are between
        # 6-10
        sub_area_letters = ['a', 'b', 'c']  # Confirming all instances are
        # between a-c
        # 'Subfile' tests not done for ALACART as videos are named in different
        # ways/formats

    # Label tests
    tag_names = ['START', 'ERR', 'N.P.', 'N.R.', 'DESC']  # Confirming all
    # instances have the given labels

    ## Carrying out tests
    # Checking 'Task Area' column. Looking there is at least one of the
    # instances in 'area_nums'
    for row in range(len(ochra)):
        if isna(ochra[row, task]):
            raise Exception("Task Area not as expected.")
    for area_name in area_nums:
        if area_name not in ochra[:, task]:
            raise Exception("Task Area not as expected.")

    # Checking 'Subtask Area' column
    for row in range(len(ochra)):
        if not isna(ochra[row, subtask]):
            if ochra[row, subtask] not in sub_area_letters:
                raise Exception("Subtask Area not as expected.")

    # Checking label column
    for row in range(len(ochra)):
        if isna(ochra[row, label]):
            raise Exception("Label not as expected.")
        elif ochra[row, label] not in tag_names:
            raise Exception("Label not as expected.")

    # Checking 'Subfile' column
    if dataset == '2d3d':
        for row in range(len(ochra)):
            if not isna(ochra[row, subfile]):
                # Testing when instance only has 1 character (e.g. '1')
                if len(ochra[row, subfile]) == 1:
                    if ochra[row, subfile] not in vid_nums:
                        raise Exception("Subfile not as expected.")
                # Testing when instance has 2 characters (e.g. '1B' or '10')
                elif len(ochra[row, subfile]) == 2:
                    if ochra[row, subfile][0:2] not in vid_nums:
                        if (ochra[row, subfile][0] not in vid_nums
                                or ochra[row, subfile][1] not in vid_letters):
                            raise Exception("Subfile not as expected.")
                # Testing when instance has 3 characters (e.g. '10B or 1AB')
                elif len(ochra[row, subfile]) == 3:
                    if (ochra[row, subfile][0] not in vid_nums
                            or ochra[row, subfile][1:3] not in vid_letters):
                        if (ochra[row, subfile][0:2] not in vid_nums
                                or ochra[row, subfile][2] not in vid_letters):
                            raise Exception("Subfile not as expected.")
                # Any other options
                else:
                    raise Exception("Subfile not as expected.")

    # Checking 'Further info' column
    for row in range(len(ochra)):
        if not isna(ochra[row, info]):
            if check_info in ochra[row, info]:
                raise Exception(f"Found '{check_info}' in Further Info.")
