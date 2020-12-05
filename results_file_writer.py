import csv
import os


def write_results_to_file(scan_results):
    if len(scan_results)==1:
        write_specific_user_result_to_file(scan_results[0])
    else:
        write_all_friends_result_to_file(scan_results)
    return


def write_specific_user_result_to_file(scan_result):
    path = os.path.dirname(__file__) + '/scan_result.csv'
    offensive = scan_result.offensiveness_result
    fakeNews = scan_result.offensiveness_result
    trigers = scan_result.trigers_result
    utv = scan_result.utv_result

    with open(path, mode='w') as result_file:
        result_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # headline
        result_writer.writerow(["", "Analysis Name","", "Percentage Result", "", "Description"])

        # write results as rows
        result_writer.writerow(["", "Offensiveness Analysis", "", offensive.percent, "", offensive.text])
        result_writer.writerow(["", "Potential Fake News Analysis", "", fakeNews.percent, "", fakeNews.text])
        result_writer.writerow(["", "Trigers Analysis", "", trigers.percent, "", trigers.text])
        result_writer.writerow(["", "Reliability Analysis", "", utv.percent, "", utv.text])
    return


def write_all_friends_result_to_file(scan_results):
    path = os.path.dirname(__file__) + '/scan_result.csv'

    with open(path, mode='w', encoding='utf-8') as result_file:
        result_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # headline
        result_writer.writerow(["", "User Name", "", "URL", "", "Offensiveness Analysis", "", "Potential Fake News Analysis", "", "Triggers Analysis", "", "Reliability Analysis"])

        # write results as rows
        for scan_result in scan_results:
            row = ["", scan_result.user_name, 
                    "", scan_result.url,
                    "", scan_result.offensiveness_result.percent,
                    "", scan_result.potentialFakeNews_result.percent,
                    "", scan_result.trigers_result.percent,
                    "", scan_result.utv_result.percent]
            result_writer.writerow(row)
    return