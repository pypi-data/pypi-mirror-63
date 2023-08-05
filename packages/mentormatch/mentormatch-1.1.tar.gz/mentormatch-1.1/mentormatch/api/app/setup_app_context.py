from __future__ import annotations
from typing import List, Dict
import mentormatch.api.initializer.initializer_implementation as _initializers
import mentormatch.utils.enums as _enums
from mentormatch.api.applicant.applicant_collection import ApplicantCollection
from mentormatch.api.applicant.applicant_factory import ApplicantFactory
from mentormatch.api.matcher import Matcher
from .setup_sorter_context_mgr import _sorters
from .setup_compatibility_checker_factory import compatibility_factory
from mentormatch.api.summarize import MatchingSummary
from mentormatch.api.applicant.applicant_implementation_mentor import Mentor
from mentormatch.api.applicant.applicant_implementation_mentee import Mentee


_MENTOR = _enums.ApplicantType.MENTOR
_MENTEE = _enums.ApplicantType.MENTEE
_PREFERRED = _enums.PairType.PREFERRED
_RANDOM = _enums.PairType.RANDOM


class Context:

    def __init__(self, mentor_dicts: List[Dict], mentee_dicts: List[Dict]):

        self._applicant_dicts = {
            _MENTOR: mentor_dicts,
            _MENTEE: mentee_dicts,
        }

        sorter_context_mgrs = _sorters

        applicant_factories = {
            _MENTOR: ApplicantFactory(
                applicant_class=Mentor,
                sorter=sorter_context_mgrs[_MENTOR]
            ),
            _MENTEE: ApplicantFactory(
                applicant_class=Mentee,
                sorter=sorter_context_mgrs[_MENTEE]
            ),
        }

        self._applicants = {
            _MENTOR: ApplicantCollection(
                applicant_dicts=self._applicant_dicts[_MENTOR],
                applicant_factory=applicant_factories[_MENTOR],
            ),
            _MENTEE: ApplicantCollection(
                applicant_dicts=self._applicant_dicts[_MENTEE],
                applicant_factory=applicant_factories[_MENTEE],
            ),
        }

        initializers = {
            _PREFERRED: _initializers.InitializerPreferred(
                mentors=self._applicants[_MENTOR],
                compatibility_checker=compatibility_factory.get_compatibility_checker(_PREFERRED),
                sorter=_sorters[_PREFERRED]
            ),
            _RANDOM: _initializers.InitializerRandom(
                mentors=self._applicants[_MENTOR],
                compatibility_checker=compatibility_factory.get_compatibility_checker(_RANDOM),
                sorter=_sorters[_RANDOM]
            ),
        }

        self._matchers = {
            _PREFERRED: Matcher(
                mentors=self._applicants[_MENTOR],
                mentees=self._applicants[_MENTEE],
                initializer=initializers[_PREFERRED],
                ranker_context_mgr=sorter_context_mgrs[_PREFERRED],
            ),
            _RANDOM: Matcher(
                mentors=self._applicants[_MENTOR],
                mentees=self._applicants[_MENTEE],
                initializer=initializers[_RANDOM],
                ranker_context_mgr=sorter_context_mgrs[_RANDOM],
            ),
        }

        self._summarizer = MatchingSummary(
            mentors=self._applicants[_MENTOR],
            mentees=self._applicants[_MENTEE],
        )

    def get_applicants(self, applicant_type: _enums.ApplicantType) -> ApplicantCollection:
        return self._applicants[applicant_type]

    def get_matcher(self, pair_type: _enums.PairType) -> Matcher:
        return self._matchers[pair_type]

    def get_summarizer(self) -> MatchingSummary:
        return self._summarizer
