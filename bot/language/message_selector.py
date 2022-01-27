# The MIT License (MIT)

# Copyright (c) Taylor Otwell

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Credits to Taylor Otwell. Original PHP code, translated to Python by me
# https://github.com/laravel/framework/blob/8e2d72728d6911816a97843ec3341e28c92af120/src/Illuminate/Translation/MessageSelector.php

from collections.abc import Iterable
from re import compile as re_compile
from typing import Any, List, Optional


class MessageSelector:
    def choose(self, line: str, number: int, locale: str) -> str:
        """
        Select a proper translation string based on the given number.

        Args:
            line (str): The line with propers translations.
            number (int): The number of items.
            locale (str): The locale to use.

        Returns:
            str: The selected translation string.

        """
        segments = line.split('|')
        value = self._extract(segments, number)
        if value is not None:
            return value.strip()

        segments = self._strip_conditions(segments)
        plural_index = self._get_plural_index(locale, number)

        if (len(segments) == 1) or (not plural_index < len(segments)):
            return segments[0].strip()

        return segments[plural_index].strip()

    def _extract(self, segments: Iterable[Any], number: int) -> Optional[str]:
        """
        Extract a translation string using inline conditions.

        Args:
            segments (Iterable[Any]): The segments of the message.
            number (int): The number of items, used to determine the plural.

        Returns:
            Optional[str]: The extracted translation string.

        """
        for part in segments:
            line = self._extract_from_string(part, number)
            if line is not None:
                return line

    @staticmethod
    def _extract_from_string(part: str, number: int) -> Optional[str]:
        """
        Get the translation string if the condition matches.

        Args:
            part (str): The part of the segments.
            number (int): The number of items.

        Returns:
            Optional[str]: The translation string.

        """
        regex = re_compile(r"^[\{\[]([^\[\]\{\}]*)[\}\]](.*)")
        matches = regex.findall(part)
        if len(matches) > 0:
            matches = matches[0]

        if len(matches) != 2:
            return None

        condition = matches[0]
        value = matches[1]

        if ',' in condition:
            from_, to = condition.split(',', 2)
            if from_ == '*':
                to = int(to)
                if number <= to:
                    return value
            elif to == '*':
                from_ = int(from_)
                if number >= from_:
                    return value
            else:
                from_ = int(from_)
                to = int(to)
                if number >= from_ and number <= to:
                    return value

        return value if condition == number else None

    @staticmethod
    def _strip_conditions(segments: Iterable[Any]) -> List[str]:
        """
        Strip the inline conditions from each segment, just leaving the text.

        Args:
            segments (Iterable[Any]): The segments of the message.

        Returns:
            List[str]: The segments without the conditions.

        """
        regex = re_compile(r"^[\{\[]([^\[\]\{\}]*)[\}\]]")
        return [regex.sub('', part) for part in segments]

    @staticmethod
    def _get_plural_index(locale: str, number: int) -> int:
        """
        Get the index to use for pluralization.

        Args:
            locale (str): The locale to use.
            number (int): The number of items.

        Returns:
            int: The plural index.

        """
        if locale in [
            'az', 'az_AZ', 'bo', 'bo_CN', 'bo_IN', 'dz', 'dz_BT', 'id', 'id_ID',
            'ja', 'ja_JP', 'jv', 'ka', 'ka_GE', 'km', 'km_KH', 'kn', 'kn_IN',
            'ko', 'ko_KR', 'ms', 'ms_MY', 'th', 'th_TH', 'tr', 'tr_CY', 'tr_TR',
            'vi', 'vi_VN', 'zh', 'zh_CN', 'zh_HK', 'zh_SG', 'zh_TW'
        ]:
            return 0
        elif locale in [
            'af', 'af_ZA', 'bn', 'bn_BD', 'bn_IN', 'bg', 'bg_BG', 'ca', 'ca_AD',
            'ca_ES', 'ca_FR', 'ca_IT', 'da', 'da_DK', 'de', 'de_AT', 'de_BE',
            'de_CH', 'de_DE', 'de_LI', 'de_LU', 'el', 'el_CY', 'el_GR', 'en',
            'en_AG', 'en_AU', 'en_BW', 'en_CA', 'en_DK', 'en_GB', 'en_HK',
            'en_IE', 'en_IN', 'en_NG', 'en_NZ', 'en_PH', 'en_SG', 'en_US',
            'en_ZA', 'en_ZM', 'en_ZW', 'eo', 'eo_US', 'es', 'es_AR', 'es_BO',
            'es_CL', 'es_CO', 'es_CR', 'es_CU', 'es_DO', 'es_EC', 'es_ES',
            'es_GT', 'es_HN', 'es_MX', 'es_NI', 'es_PA', 'es_PE', 'es_PR',
            'es_PY', 'es_SV', 'es_US', 'es_UY', 'es_VE', 'et', 'et_EE', 'eu',
            'eu_ES', 'eu_FR', 'fa', 'fa_IR', 'fi', 'fi_FI', 'fo', 'fo_FO',
            'fur', 'fur_IT', 'fy', 'fy_DE', 'fy_NL', 'gl', 'gl_ES', 'gu',
            'gu_IN', 'ha', 'ha_NG', 'he', 'he_IL', 'hu', 'hu_HU', 'is', 'is_IS',
            'it', 'it_CH', 'it_IT', 'ku', 'ku_TR', 'lb', 'lb_LU', 'ml', 'ml_IN',
            'mn', 'mn_MN', 'mr', 'mr_IN', 'nah', 'nb', 'nb_NO', 'ne', 'ne_NP',
            'nl', 'nl_AW', 'nl_BE', 'nl_NL', 'nn', 'nn_NO', 'no', 'om', 'om_ET',
            'om_KE', 'or', 'or_IN', 'pa', 'pa_IN', 'pa_PK', 'pap', 'pap_AN',
            'pap_AW', 'pap_CW', 'ps', 'ps_AF', 'pt', 'pt_BR', 'pt_PT', 'so',
            'so_DJ', 'so_ET', 'so_KE', 'so_SO', 'sq', 'sq_AL', 'sq_MK', 'sv',
            'sv_FI', 'sv_SE', 'sw', 'sw_KE', 'sw_TZ', 'ta', 'ta_IN', 'ta_LK',
            'te', 'te_IN', 'tk', 'tk_TM', 'ur', 'ur_IN', 'ur_PK', 'zu', 'zu_ZA'
        ]:
            return 0 if number == 1 else 1
        elif locale in [
            'am', 'am_ET', 'bh', 'fil', 'fil_PH', 'fr', 'fr_BE', 'fr_CA',
            'fr_CH', 'fr_FR', 'fr_LU', 'gun', 'hi', 'hi_IN', 'hy', 'hy_AM',
            'ln', 'ln_CD', 'mg', 'mg_MG', 'nso', 'nso_ZA', 'ti', 'ti_ER',
            'ti_ET', 'wa', 'wa_BE', 'xbr'
        ]:
            return 0 if (number == 0 or number == 1) else 1
        elif locale in [
            'be', 'be_BY', 'bs', 'bs_BA', 'hr', 'hr_HR', 'ru', 'ru_RU', 'ru_UA',
            'sr', 'sr_ME', 'sr_RS', 'uk', 'uk_UA'
        ]:
            if (number % 10 == 1) and (number % 100 != 11):
                return 0
            elif (number % 10 >= 2) and (number % 10 <= 4) and (
                (number % 100 < 10) or (number % 100 >= 20)
            ):
                return 1
            else:
                return 2
        elif locale in ['cs', 'cs_CZ', 'sk', 'sk_SK']:
            if number == 1:
                return 0
            elif number >= 2 and number <= 4:
                return 1
            else:
                return 2
            return 0
        elif locale in ['ga', 'ga_IE']:
            if number == 1:
                return 0
            elif number == 2:
                return 1
            else:
                return 2
        elif locale in ['lt', 'lt_LT']:
            if (number % 10 == 1) and (number % 100 != 11):
                return 0
            elif (number % 10 >= 2) and (number % 100 <
                                         10) or (number % 100 >= 20):
                return 1
            else:
                return 2
        elif locale in ['sl', 'sl_SI']:
            if number % 100 == 1:
                return 0
            elif number % 100 == 2:
                return 1
            elif (number % 100 == 3) or (number % 100 == 4):
                return 2
            else:
                return 3
        elif locale in ['mk', 'mk_MK']:
            return 0 if number % 10 == 1 else 1
        elif locale in ['mt', 'mt_MT']:
            if number == 1:
                return 0
            elif (number == 0) or ((number % 100 > 1) and (number % 100 < 11)):
                return 1
            elif (number % 100 > 10) and (number % 100 < 20):
                return 2
            else:
                return 3
        elif locale in ['lv', 'lv_LV']:
            if number == 0:
                return 0
            elif (number % 10 == 1) and (number % 100 != 11):
                return 1
            else:
                return 2
        elif locale in ['pl', 'pl_PL']:
            if number == 1:
                return 0
            elif (number % 10 >= 2) and (number % 10 <= 4) and (
                (number % 100 < 12) or (number % 100 > 14)
            ):
                return 1
            else:
                return 2
        elif locale in ['cy', 'cy_GB']:
            if number == 1:
                return 0
            elif number == 2:
                return 1
            elif (number == 8) or (number == 11):
                return 2
            else:
                return 3
        elif locale in ['ro', 'ro_RO']:
            if number == 1:
                return 0
            elif (number == 0) or ((number % 100 > 0) and (number % 100 < 20)):
                return 1
            else:
                return 2
        elif locale in [
            'ar', 'ar_AE', 'ar_BH', 'ar_DZ', 'ar_EG', 'ar_IN', 'ar_IQ', 'ar_JO',
            'ar_KW', 'ar_LB', 'ar_LY', 'ar_MA', 'ar_OM', 'ar_QA', 'ar_SA',
            'ar_SD', 'ar_SS', 'ar_SY', 'ar_TN', 'ar_YE'
        ]:
            if number == 0:
                return 0
            elif number == 1:
                return 1
            elif number == 2:
                return 2
            elif (number % 100 >= 3) and (number % 100 <= 10):
                return 3
            elif (number % 100 >= 11) and (number % 100 <= 99):
                return 4
            else:
                return 5
        else:
            return 0
