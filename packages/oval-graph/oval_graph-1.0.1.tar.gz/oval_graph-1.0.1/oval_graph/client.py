import re
import argparse
import tempfile
import os
import webbrowser
import json
import shutil
from datetime import datetime
import sys

from .xml_parser import XmlParser


class Client():
    def __init__(self, args):
        self.parser = None
        self.MESSAGES = self._get_message()
        self.arg = self.parse_arguments(args)
        self.hide_passing_tests = self.arg.hide_passing_tests
        self.source_filename = self.arg.source_filename
        self.rule_name = self.arg.rule_id
        self.out = self.arg.output
        self.all_rules = self.arg.all
        self.isatty = sys.stdout.isatty()
        self.show_fail_rules = False
        self.show_not_selected_rules = False
        self.xml_parser = XmlParser(
            self.source_filename)
        self.parts = self.get_src('parts')

    def _get_message(self):
        MESSAGES = {
            'description': '',
            '--output': '',
            'source_filename': '',
        }
        return MESSAGES

    def run_gui_and_return_answers(self):
        if self.isatty:
            if self.all_rules:
                return {'rules': [
                    rule['id_rule'] for rule in self.search_rules_id()]}
            else:
                try:
                    import inquirer
                    return inquirer.prompt(self.get_questions())
                except ImportError:
                    print(self.get_selection_rules())
                    return None
        else:
            return {'rules': [
                rule['id_rule'] for rule in self.search_rules_id()]}

    def get_list_of_matched_rules(self):
        rules = self.search_rules_id()
        if self.show_fail_rules:
            rules = self._get_only_fail_rule(rules)
        return rules

    def get_list_of_lines(self):
        lines = ['== The Rule IDs ==']
        for rule in self.get_list_of_matched_rules():
            lines.append("'" + rule['id_rule'] + r'\b' + "'")
        if self.show_not_selected_rules:
            for line in self.get_lines_of_wanted_not_selected_rules():
                lines.append(line)
        lines.append(
            "You haven't got installed inquirer lib. "
            "Please copy id rule with you want use and put it in command")
        return lines

    def get_selection_rules(self):
        return "\n".join(self.get_list_of_lines())

    def get_lines_of_wanted_not_selected_rules(self):
        out = []
        out.append('== The not selected rule IDs ==')
        for rule in self._get_wanted_not_selected_rules():
            out.append(rule['id_rule'] + '(Not selected)')
        return out

    def get_choices(self):
        rules = self.search_rules_id()
        if self.show_fail_rules:
            rules = self._get_only_fail_rule(rules)
        choices = []
        for rule in rules:
            choices.append(rule['id_rule'])
        if self.show_not_selected_rules:
            print("\n".join(self.get_lines_of_wanted_not_selected_rules()))
        return choices

    def get_questions(self):
        choices = self.get_choices()
        from inquirer.questions import Checkbox as checkbox
        questions = [
            checkbox(
                'rules',
                message=(
                    "= The Rules IDs = (move - UP and DOWN arrows,"
                    " select - SPACE or LEFT and RIGHT arrows, submit - ENTER)"),
                choices=choices,
            ),
        ]
        return questions

    def _get_only_fail_rule(self, rules):
        return list(filter(lambda rule: rule['result'] == 'fail', rules))

    def _get_wanted_rules(self):
        return [
            x for x in self.xml_parser.used_rules if re.search(
                self.rule_name, x['id_rule'])]

    def _get_wanted_not_selected_rules(self):
        return [
            x for x in self.xml_parser.notselected_rules if re.search(
                self.rule_name, x['id_rule'])]

    def search_rules_id(self):
        rules = self._get_wanted_rules()
        notselected_rules = self._get_wanted_not_selected_rules()
        if len(notselected_rules) and not rules:
            raise ValueError(
                ('err- rule(s) "{}" was not selected, '
                 "so there are no results. The rule is"
                 ' "notselected" because it'
                 " wasn't a part of the executed profile"
                 " and therefore it wasn't evaluated "
                 "during the scan.")
                .format(notselected_rules[0]['id_rule']))
        elif not notselected_rules and not rules:
            raise ValueError('err- 404 rule not found!')
        else:
            return rules

    def open_web_browser(self, src):
        if not self.off_webbrowser:
            try:
                webbrowser.get('firefox').open_new_tab(src)
            except BaseException:
                webbrowser.open_new_tab(src)

    def get_src(self, src):
        _dir = os.path.dirname(os.path.realpath(__file__))
        FIXTURE_DIR = os.path.join(_dir, src)
        return str(FIXTURE_DIR)

    def get_save_src(self, rule):
        date = str(datetime.now().strftime("-%d_%m_%Y-%H_%M_%S"))
        if self.out is not None:
            os.makedirs(self.out, exist_ok=True)
            return os.path.join(
                self.out,
                'graph-of-' + rule + date + '.html')
        return os.path.join(
            os.getcwd(),
            'graph-of-' + rule + date + '.html')

    def _get_head(self):
        with open(os.path.join(self.parts, 'head.html'), "r") as data_file:
            head = data_file.readlines()
        return head

    def _get_footer(self):
        with open(os.path.join(self.parts, 'footer.html'), "r") as data_file:
            footer = data_file.readlines()
        return footer

    def _merge_report_parts(self, data):
        head = self._get_head()
        footer = self._get_footer()
        return [*head, data, *footer]

    def save_html_report(self, dict_, src):
        data = "var data_of_tree =" + str(
            json.dumps(dict_, sort_keys=False, indent=4) + ";")
        with open(src, "w+") as data_file:
            data_file.writelines(self._merge_report_parts(data))

    def parse_arguments(self, args):
        self.prepare_parser()
        args = self.parser.parse_args(args)
        return args

    def prepare_parser(self):
        self.parser = argparse.ArgumentParser(
            description=self.MESSAGES.get('description'))
        self.parser.add_argument(
            '--all',
            action="store_true",
            default=False,
            help="Process all matched rules.")
        self.parser.add_argument(
            '--hide-passing-tests',
            action="store_true",
            default=False,
            help=(
                "Do not display passing tests for better orientation in"
                " graphs that contain a large amount of nodes.(Not implemented)"))
        self.parser.add_argument(
            '-o',
            '--output',
            action="store",
            default=None,
            help=self.MESSAGES.get('--output'))
        self.parser.add_argument(
            "source_filename",
            help=self.MESSAGES.get('source_filename'))
        self.parser.add_argument(
            "rule_id", help=(
                "Rule ID to be visualized. A part from the full rule ID"
                " a part of the ID or a regular expression can be used."
                " If brackets are used in the regular expression "
                "the regular expression must be quoted."))
