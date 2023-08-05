from typing import List
import pandas as pd

from ..desiredstate import DesiredState
from ..decisions import Decisions
from ..reduction import Reduction
from ..arules import ActionRules


class ActionRulesDiscovery:
    """
    ActionRulesDiscovery class
    """
    ACTION_RULE = "action rule"
    ACTION_RULE_TARGET = "action rule target"
    SUPPORT_BEFORE = "support before"
    SUPPORT_AFTER = "support after"
    ACTION_RULE_SUPPORT = "action rule support"
    CONFIDENCE_BEFORE = "confidence before"
    CONFIDENCE_AFTER = "confidence after"
    ACTION_RULE_CONFIDENCE = "action rule confidence"
    ACTION_RULE_UPLIFT = "uplift"
    RECOMMENDED = "-recommended"

    def __init__(self):
        """
        Initialise
        """
        self.decisions = Decisions()
        self.arules = None
        self.desired_state = None
        self.stable_antecedents = []
        self.flexible_antecedents = []
        self.consequent = ""

    def check_columns(self, antecedents: list, consequent: str):
        """
        Check if valid.
        """
        if len(self.decisions.data) == 0:
            raise Exception("No data entered.")
        columns = self.decisions.data.columns
        for col_name in antecedents + [consequent]:
            if col_name not in columns:
                raise Exception("Column " + str(col_name) + " does not exist in data")

    def read_csv(self, file: str, **kwargs):
        """
        Create data frame from csv.
        """
        self.decisions.read_csv(file, **kwargs)

    def load_pandas(self, data_frame: pd.DataFrame):
        """
        Load data frame.
        """
        self.decisions.load_pandas(data_frame)

    def fit(self,
            stable_antecedents: List[str],
            flexible_antecedents: List[str],
            consequent: str,
            conf: float,
            supp: float,
            desired_classes: List[str] = None,
            desired_changes: List[list] = None,
            is_nan: bool = False,
            is_reduction: bool = True,
            min_stable_antecedents: int = 1,
            min_flexible_antecedents: int = 1,
            max_stable_antecedents: int = 5,
            max_flexible_antecedents: int = 5,
            ):
        """
        Get action rules.
        Define antecedent and consequent.
        - stable_antecedents - List of column names.
        - flexible_antecedents - List of column names.
        - consequent - Name of the consequent column.
        Confidence and support.
        - conf - Value in % for minimal confidence in classification rules.
                 For example, 60.
        - supp - Value in % for minimal support of classification rules.
                 For example, 5.
        Desired classes or desired changes must be entered.
        - desired_classes - List of decision states. For example, ["1"].
                            DEFAULT: None
        - desired_changes - List of desired changes. For example, [["0", "1"]].
                            DEFAULT: None
        Should NaN values be used?
        - is_nan - True means NaN values are used, False means NaN values are not used.
                   DEFAULT: FALSE
        Should the reduction table be used?
        - is_reduction - Is the reduction table used? DEFAULT: TRUE
        Minimal number of stable and flexible pairs in antecedent.
        - min_stable_antecedents - Minimal number of stable pairs. DEFAULT: 1
        - min_flexible_antecedents - Minimal number of flexible pairs. DEFAULT: 1
        - max_stable_antecedents - Maximal number of stable pairs. DEFAULT: 5
        - max_flexible_antecedents - Maximal number of flexible pairs. DEFAULT: 5
        """
        if (self.arules):
            raise Exception("Fit was already called")
        self.stable_antecedents = stable_antecedents
        self.flexible_antecedents = flexible_antecedents
        self.consequent = consequent
        if bool(desired_classes) != bool(desired_changes):
            self.desired_state = DesiredState(desired_classes=desired_classes, desired_changes=desired_changes)
        else:
            raise Exception("Desired classes or desired changes must be entered")
        antecedents = stable_antecedents + flexible_antecedents
        self.check_columns(antecedents, consequent)
        self.decisions.prepare_data_fim(antecedents, consequent)
        self.decisions.fit_fim_apriori(conf=conf, support=supp)
        self.decisions.generate_decision_table()
        stable = self.decisions.decision_table[stable_antecedents]
        flex = self.decisions.decision_table[flexible_antecedents]
        target = self.decisions.decision_table[[consequent]]
        supp = self.decisions.support
        conf = self.decisions.confidence
        reduced_tables = Reduction(stable, flex, target, self.desired_state, supp, conf, is_nan)
        if is_reduction:
            reduced_tables.reduce()
        self.arules = ActionRules(
            reduced_tables.stable_tables,
            reduced_tables.flexible_tables,
            reduced_tables.decision_tables,
            self.desired_state,
            reduced_tables.supp,
            reduced_tables.conf,
            is_nan,
            min_stable_antecedents,
            min_flexible_antecedents,
            max_stable_antecedents,
            max_flexible_antecedents
        )
        self.arules.fit()

    def fit_classification_rules(self,
                                 stable_antecedents: List[str],
                                 flexible_antecedents: List[str],
                                 consequent: str,
                                 conf_col: str,
                                 supp_col: str,
                                 desired_classes: List[str] = None,
                                 desired_changes: List[list] = None,
                                 is_nan: bool = False,
                                 is_reduction: bool = True,
                                 min_stable_antecedents: int = 1,
                                 min_flexible_antecedents: int = 1,
                                 max_stable_antecedents: int = 5,
                                 max_flexible_antecedents: int = 5,
                                 ):
        """
        Get action rules.
        Define antecedent and consequent.
        - stable_antecedents - List of column names.
        - flexible_antecedents - List of column names.
        - consequent - Name of the consequent column.
        Confidence and support.
        - conf_col - Name of the column with classification rule confidence -
                     the numbers should be in form 0.1 for 10%.
        - supp_col - Name of the column with classification rule support -
                     the numbers should be in form 0.1 for 10%.
        Desired classes or desired changes must be entered.
        - desired_classes - List of decision states. For example ["1"].
                            DEFAULT: None
        - desired_changes - List of desired changes. For example [["0", "1"]].
                            DEFAULT: None
        Should NaN values be used?
        - is_nan - True means NaN values are used, False means nan values are not used.
                   DEFAULT: FALSE
        Should the reduction table be used?
        - is_reduction - Is the reduction table used? DEFAULT: TRUE
        Minimal number of stable and flexible pairs in antecedent.
        - min_stable_antecedents - Minimal number of stable pairs. DEFAULT: 1
        - min_flexible_antecedents - Minimal number of flexible pairs. DEFAULT: 1
        - max_stable_antecedents - Maximal number of stable pairs. DEFAULT: 5
        - max_flexible_antecedents - Maximal number of flexible pairs. DEFAULT: 5
        """
        if (self.arules):
            raise Exception("Fit was already called")
        self.stable_antecedents = stable_antecedents
        self.flexible_antecedents = flexible_antecedents
        self.consequent = consequent
        if bool(desired_classes) != bool(desired_changes):
            self.desired_state = DesiredState(desired_classes=desired_classes, desired_changes=desired_changes)
        else:
            raise Exception("Desired classes or desired changes must be entered")
        antecedents = stable_antecedents + flexible_antecedents
        self.check_columns(antecedents, consequent)
        stable = self.decisions.data[stable_antecedents]
        flex = self.decisions.data[flexible_antecedents]
        target = self.decisions.data[[consequent]]
        supp_df = self.decisions.data[[supp_col]]
        supp_series = supp_df.iloc[:, 0]
        supp = supp_series.tolist()
        conf_df = self.decisions.data[[conf_col]]
        conf_series = conf_df.iloc[:, 0]
        conf = conf_series.tolist()
        reduced_tables = Reduction(stable, flex, target, self.desired_state, supp, conf, is_nan)
        if is_reduction:
            reduced_tables.reduce()
        self.arules = ActionRules(
            reduced_tables.stable_tables,
            reduced_tables.flexible_tables,
            reduced_tables.decision_tables,
            self.desired_state,
            reduced_tables.supp,
            reduced_tables.conf,
            is_nan,
            min_stable_antecedents,
            min_flexible_antecedents,
            max_stable_antecedents,
            max_flexible_antecedents
        )
        self.arules.fit()

    def get_action_rules(self) -> list:
        """
        Get action rules.
        """
        return self.arules.action_rules

    def get_pretty_action_rules(self) -> list:
        """
        Get pretty text of action rules.
        """
        if len(self.arules.action_rules_pretty_text) == 0:
            self.arules.pretty_text()
        return self.arules.action_rules_pretty_text

    def get_action_rules_representation(self) -> list:
        """
        Get representation of action rules.
        """
        if len(self.arules.action_rules_representation) == 0:
            self.arules.representation()
        return self.arules.action_rules_representation

    def get_source_data_for_ar(self, action_r_number: int, is_before: bool) -> pd.DataFrame:
        """
        Get dataframe with values which action rule is based on
        - action_r_number - Action rule number.
        - is_before - Distinguish the rules before (True) or after (False)
        """
        if is_before:
            classification = self.arules.classification_before[action_r_number]
        else:
            classification = self.arules.classification_after[action_r_number]
        decision = self.decisions.decision_table.loc[
            classification, self.stable_antecedents + self.flexible_antecedents]
        source_table = self._reduce_table_source(decision, self.decisions.data)
        return source_table.style.applymap(lambda x: 'background-color: yellow',
                                           subset=self.stable_antecedents) \
            .applymap(lambda x: 'background-color: orange',
                      subset=self.flexible_antecedents) \
            .applymap(lambda x: 'color: green' if x in self.desired_state.get_destination_classes() else 'color: red',
                      subset=[self.consequent])

    @staticmethod
    def _reduce_table_source(decision: pd.Series, source_table: pd.DataFrame) -> pd.DataFrame:
        """
        Get dataframe by classification rule.
        - decision - Classification rule
        """
        new_data = source_table.applymap(str).copy()
        for key, value in decision.items():
            if str(value) != "nan":
                mask = new_data[key] == value
                new_data = new_data[mask]
        return new_data

    def predict(self, source_table: pd.DataFrame):
        """
        Predict if any values would need to change their state.
        - table for prediction
        """
        i = 0
        full_predicted_table = pd.DataFrame()
        for classification_before in self.arules.classification_before:
            classification_after = self.arules.classification_after[i]
            decision_before = self.decisions.decision_table.loc[
                classification_before, self.stable_antecedents + self.flexible_antecedents]
            decision_after = self.decisions.decision_table.loc[
                classification_after, self.stable_antecedents + self.flexible_antecedents]
            predicted_table = self._reduce_table_source(decision_before, source_table)
            if len(predicted_table.index) > 0:
                for key, value in decision_after.items():
                    if str(value) != "nan" and key in self.flexible_antecedents:
                        column = key + self.RECOMMENDED
                        predicted_table[column] = [value] * len(predicted_table.index)
                        predicted_table[self.ACTION_RULE] = [i] * len(predicted_table.index)
                        predicted_table = predicted_table.astype({self.ACTION_RULE: int})
                predicted_table[self.ACTION_RULE_TARGET] = \
                    [self.arules.action_rules[i][0][2][1][1]] * len(predicted_table.index)
                predicted_table[self.SUPPORT_BEFORE] = \
                    [self.arules.action_rules[i][1][0]] * len(predicted_table.index)
                predicted_table[self.SUPPORT_AFTER] = \
                    [self.arules.action_rules[i][1][1]] * len(predicted_table.index)
                predicted_table[self.ACTION_RULE_SUPPORT] = \
                    [self.arules.action_rules[i][1][2]] * len(predicted_table.index)
                predicted_table[self.CONFIDENCE_BEFORE] = \
                    [self.arules.action_rules[i][2][0]] * len(predicted_table.index)
                predicted_table[self.CONFIDENCE_AFTER] = \
                    [self.arules.action_rules[i][2][1]] * len(predicted_table.index)
                predicted_table[self.ACTION_RULE_CONFIDENCE] = \
                    [self.arules.action_rules[i][2][2]] * len(predicted_table.index)
                predicted_table[self.ACTION_RULE_UPLIFT] = \
                    [self.arules.action_rules[i][3]] * len(predicted_table.index)
            full_predicted_table = pd.concat([full_predicted_table, predicted_table], sort=True)
            i += 1
        # New columns always in the end
        cols = full_predicted_table.columns.tolist()
        if len(cols)>0:
            cols.append(cols.pop(cols.index(self.ACTION_RULE)))
            cols.append(cols.pop(cols.index(self.ACTION_RULE_TARGET)))
            cols.append(cols.pop(cols.index(self.SUPPORT_BEFORE)))
            cols.append(cols.pop(cols.index(self.SUPPORT_AFTER)))
            cols.append(cols.pop(cols.index(self.ACTION_RULE_SUPPORT)))
            cols.append(cols.pop(cols.index(self.CONFIDENCE_BEFORE)))
            cols.append(cols.pop(cols.index(self.CONFIDENCE_AFTER)))
            cols.append(cols.pop(cols.index(self.ACTION_RULE_CONFIDENCE)))
            cols.append(cols.pop(cols.index(self.ACTION_RULE_UPLIFT)))
            full_predicted_table = full_predicted_table[cols]
        return full_predicted_table
