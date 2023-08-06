from __future__ import annotations

import time
from typing import TYPE_CHECKING, Dict, List, Optional

import halo

from pdm.iostream import stream

if TYPE_CHECKING:
    from pdm.models.candidates import Candidate
    from pdm.models.requirements import Requirement
    from pdm.resolver.resolvers import State


def print_title(title):
    print("=" * 20 + " " + title + " " + "=" * 20)


class SimpleReporter:
    def __init__(self, requirements: List[Requirement]) -> None:
        self.requirements = requirements
        self.start_at = None  # type: Optional[float]
        self._previous = None  # type: Optional[Dict[str, Candidate]]

    def starting_round(self, index: int) -> None:
        pass

    def starting(self) -> None:
        """Called before the resolution actually starts.
        """
        self._previous = None
        print_title("Start resolving requirements...")
        self.start_at = time.time()
        for r in self.requirements:
            print(r.as_line())

    def ending_round(self, index: int, state: State) -> None:
        """Called before each round of resolution ends.

        This is NOT called if the resolution ends at this round. Use `ending`
        if you want to report finalization. The index is zero-based.
        """
        print_title(f"Ending ROUND {index}")

        if not self._previous:
            added = state.mapping.values()
            changed = []
        else:
            added = [can for k, can in state.mapping.items() if k not in self._previous]
            changed = [
                (self._previous[k], can)
                for k, can in state.mapping.items()
                if k in self._previous and self._previous[k] != can
            ]
        if added:
            print("New pins:")
            for can in added:
                print(f"\t{can.name}\t{can.version}")
        if changed:
            print("Changed pins:")
            for (old, new) in changed:
                print(f"\t{new.name}\t{old.version} -> {new.version}")
        self._previous = state.mapping

    def ending(self, state: State) -> None:
        """Called before the resolution ends successfully.
        """
        print("End resolving...")
        print("Stable pins:")
        for k, can in state.mapping.items():
            print(f"\t{can.name}\t{can.version}")

    def resolve_criteria(self, name):
        pass

    def pin_candidate(self, name, criterion, candidate, child_names):
        pass

    def extract_metadata(self):
        pass


class SpinnerReporter:
    def __init__(self, spinner: halo.Halo) -> None:
        self.spinner = spinner

    def starting_round(self, index: int) -> None:
        # self.spinner.hide_and_write(f"Resolving ROUND {index}")
        pass

    def starting(self) -> None:
        """Called before the resolution actually starts.
        """

    def ending_round(self, index: int, state: State) -> None:
        """Called before each round of resolution ends.

        This is NOT called if the resolution ends at this round. Use `ending`
        if you want to report finalization. The index is zero-based.
        """

    def ending(self, state: State) -> None:
        """Called before the resolution ends successfully.
        """
        self.spinner.stop_and_persist(text="Finish resolving")

    def resolve_criteria(self, name):
        self.spinner.text = f"Resolving {stream.green(name, bold=True)}"

    def pin_candidate(self, name, criterion, candidate, child_names):
        self.spinner.text = f"Resolved: {candidate.format()}"

    def extract_metadata(self):
        self.spinner.start("Extracting package metadata")
