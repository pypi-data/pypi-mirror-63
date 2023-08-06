#!/use/bin/python
# --*-- coding: utf-8 --*--

# !!! Will work only on Python 3 and above

import pandas as pd
import nwae.utils.Log as lg
from inspect import getframeinfo, currentframe
# from iso639 import languages


#
# Class LangFeatures
#
#   Helper class to define language properties, such as containing word/syllable separators,
#   alphabet type, etc.
#
class LangFeatures:

    #
    # TODO
    #  Move to use ISO 639-2 standard instead of our own
    #
    LANG_EN = 'en'
    # Simplified Chinese
    LANG_CN = 'cn'
    LANG_ZH_CN = 'zh-cn'
    # Thai
    LANG_TH = 'th'
    # Vietnamese
    LANG_VN = 'vn'
    LANG_VI = 'vi'
    # Indonesian
    LANG_IN = 'in'
    # Korean
    LANG_KO = 'ko'
    # French
    LANG_FR = 'fr'
    # Russian
    LANG_RU = 'ru'

    C_LANG_ID        = 'Language'
    C_LANG_NAME      = 'LanguageName'
    C_HAVE_ALPHABET  = 'Alphabet'
    C_CHAR_TYPE      = 'CharacterType'
    C_HAVE_SYL_SEP   = 'SyllableSep'
    C_SYL_SEP_TYPE   = 'SyllableSepType'
    C_HAVE_WORD_SEP  = 'WordSep'
    C_WORD_SEP_TYPE  = 'WordSepType'
    C_HAVE_VERB_CONJ = 'HaveVerbConjugation'

    T_NONE = ''
    T_CHAR = 'character'
    T_SPACE = 'space'

    LEVEL_ALPHABET = 'alphabet'
    LEVEL_SYLLABLE = 'syllable'
    LEVEL_UNIGRAM  = 'unigram'

    @staticmethod
    def map_to_correct_lang_code(
            lang_code
    ):
        if lang_code == LangFeatures.LANG_CN:
            return LangFeatures.LANG_ZH_CN
        elif lang_code == LangFeatures.LANG_VN:
            return LangFeatures.LANG_VI
        else:
            return lang_code

    # Word lists and stopwords are in the same folder
    def __init__(self):
        #
        # Language followed by flag for alphabet boundary, syllable boundary (either as one
        # character as in Chinese or space as in Korean), then word boundary (space)
        # The most NLP-inconvenient languages are those without word boundary, obviously.
        # Name, Code, Alphabet, CharacterType, SyllableSeparator, SyllableSeparatorType, WordSeparator, WordSeparatorType
        #
        lang_en = {
            LangFeatures.C_LANG_ID:       LangFeatures.LANG_EN,
            LangFeatures.C_LANG_NAME:     'English',
            LangFeatures.C_HAVE_ALPHABET: True,
            LangFeatures.C_CHAR_TYPE:     'latin',
            LangFeatures.C_HAVE_SYL_SEP:  False,
            LangFeatures.C_SYL_SEP_TYPE:  LangFeatures.T_NONE,
            LangFeatures.C_HAVE_WORD_SEP: True,
            LangFeatures.C_WORD_SEP_TYPE: LangFeatures.T_SPACE,
            LangFeatures.C_HAVE_VERB_CONJ: True
        }
        lang_ko = {
            LangFeatures.C_LANG_ID:       LangFeatures.LANG_KO,
            LangFeatures.C_LANG_NAME:     'Hangul',
            LangFeatures.C_HAVE_ALPHABET: True,
            LangFeatures.C_CHAR_TYPE:     'ko',
            LangFeatures.C_HAVE_SYL_SEP:  True,
            # TODO Not really right to say it is char but rather a "syllable_character"
            LangFeatures.C_SYL_SEP_TYPE:  LangFeatures.T_CHAR,
            LangFeatures.C_HAVE_WORD_SEP: True,
            LangFeatures.C_WORD_SEP_TYPE: LangFeatures.T_SPACE,
            LangFeatures.C_HAVE_VERB_CONJ: True
        }
        lang_cn = {
            LangFeatures.C_LANG_ID:       LangFeatures.LANG_CN,
            LangFeatures.C_LANG_NAME:     'Chinese',
            LangFeatures.C_HAVE_ALPHABET: False,
            LangFeatures.C_CHAR_TYPE:     'cn',
            LangFeatures.C_HAVE_SYL_SEP:  True,
            LangFeatures.C_SYL_SEP_TYPE:  LangFeatures.T_CHAR,
            LangFeatures.C_HAVE_WORD_SEP: False,
            LangFeatures.C_WORD_SEP_TYPE: LangFeatures.T_NONE,
            LangFeatures.C_HAVE_VERB_CONJ: False
        }
        lang_ru = {
            LangFeatures.C_LANG_ID:       LangFeatures.LANG_RU,
            LangFeatures.C_LANG_NAME:     'Russian',
            LangFeatures.C_HAVE_ALPHABET: True,
            LangFeatures.C_CHAR_TYPE:     'cyrillic',
            LangFeatures.C_HAVE_SYL_SEP:  False,
            LangFeatures.C_SYL_SEP_TYPE:  LangFeatures.T_NONE,
            LangFeatures.C_HAVE_WORD_SEP: True,
            LangFeatures.C_WORD_SEP_TYPE: LangFeatures.T_SPACE,
            LangFeatures.C_HAVE_VERB_CONJ: True
        }
        lang_th = {
            LangFeatures.C_LANG_ID:       LangFeatures.LANG_TH,
            LangFeatures.C_LANG_NAME:     'Thai',
            LangFeatures.C_HAVE_ALPHABET: True,
            LangFeatures.C_CHAR_TYPE:     'th',
            LangFeatures.C_HAVE_SYL_SEP:  False,
            LangFeatures.C_SYL_SEP_TYPE:  LangFeatures.T_NONE,
            LangFeatures.C_HAVE_WORD_SEP: False,
            LangFeatures.C_WORD_SEP_TYPE: LangFeatures.T_NONE,
            LangFeatures.C_HAVE_VERB_CONJ: False
        }
        lang_vn = {
            LangFeatures.C_LANG_ID:       LangFeatures.LANG_VN,
            LangFeatures.C_LANG_NAME:     'Vietnamese',
            LangFeatures.C_HAVE_ALPHABET: True,
            LangFeatures.C_CHAR_TYPE:     'latin',
            LangFeatures.C_HAVE_SYL_SEP:  True,
            LangFeatures.C_SYL_SEP_TYPE:  LangFeatures.T_SPACE,
            LangFeatures.C_HAVE_WORD_SEP: False,
            LangFeatures.C_WORD_SEP_TYPE: LangFeatures.T_NONE,
            LangFeatures.C_HAVE_VERB_CONJ: False
        }
        lang_in = {
            LangFeatures.C_LANG_ID:       LangFeatures.LANG_IN,
            LangFeatures.C_LANG_NAME:     'Indonesian',
            LangFeatures.C_HAVE_ALPHABET: True,
            LangFeatures.C_CHAR_TYPE:     'latin',
            LangFeatures.C_HAVE_SYL_SEP:  False,
            LangFeatures.C_SYL_SEP_TYPE:  LangFeatures.T_NONE,
            LangFeatures.C_HAVE_WORD_SEP: True,
            LangFeatures.C_WORD_SEP_TYPE: LangFeatures.T_SPACE,
            LangFeatures.C_HAVE_VERB_CONJ: True
        }
        self.langs = {
            LangFeatures.LANG_EN: lang_en,
            LangFeatures.LANG_KO: lang_ko,
            LangFeatures.LANG_CN: lang_cn,
            LangFeatures.LANG_RU: lang_ru,
            LangFeatures.LANG_TH: lang_th,
            LangFeatures.LANG_VN: lang_vn,
            LangFeatures.LANG_IN: lang_in
        }
        self.langfeatures = pd.DataFrame(
            self.langs.values()
        )
        return

    def __check_lang(self, lang):
        if lang not in self.langs.keys():
            raise Exception(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': No such language "' + str(lang) + '" in supported languages ' + str(self.langs.keys())
            )

    def get_word_separator_type(
            self,
            lang
    ):
        self.__check_lang(lang = lang)
        lang_dict = self.langs[lang]
        return lang_dict[LangFeatures.C_WORD_SEP_TYPE]

    def get_syllable_separator_type(
            self,
            lang
    ):
        self.__check_lang(lang = lang)
        lang_dict = self.langs[lang]
        return lang_dict[LangFeatures.C_SYL_SEP_TYPE]

    def have_verb_conjugation(
            self,
            lang
    ):
        self.__check_lang(lang = lang)
        lang_dict = self.langs[lang]
        return lang_dict[LangFeatures.C_HAVE_VERB_CONJ]

    def is_lang_token_same_with_charset(self, lang):
        # Languages that have the tokens as the character set, or languages with no syllable or unigram separator
        # Besides cn/th, the same goes for Lao, Cambodian, Japanese, with no spaces to separate syllables/unigrams.
        lf = self.langfeatures
        len = lf.shape[0]
        # First it must not have a word separator
        langindexes = [ x for x in range(0,len,1) if lf[LangFeatures.C_HAVE_WORD_SEP][x]==False ]
        # Second condition is that it doesn't have a syllable separator, or it has a syllable separator which is a character
        langs = [
            lf[LangFeatures.C_LANG_ID][x] for x in langindexes if (
                    lf[LangFeatures.C_HAVE_SYL_SEP][x]==False or
                    ( lf[LangFeatures.C_HAVE_SYL_SEP][x]==True and lf[LangFeatures.C_SYL_SEP_TYPE][x]==LangFeatures.T_CHAR )
            )
        ]
        return lang in langs

    def get_languages_with_word_separator(self):
        len = self.langfeatures.shape[0]
        langs = [ self.langfeatures[LangFeatures.C_LANG_ID][x] for x in range(0,len,1)
                  if self.langfeatures[LangFeatures.C_HAVE_WORD_SEP][x]==True ]
        return langs

    def get_languages_with_syllable_separator(self):
        len = self.langfeatures.shape[0]
        langs = [ self.langfeatures[LangFeatures.C_LANG_ID][x] for x in range(0, len, 1)
                  if self.langfeatures[LangFeatures.C_HAVE_SYL_SEP][x]==True ]
        return langs

    def get_languages_with_only_syllable_separator(self):
        return list(
            set( self.get_languages_with_syllable_separator() ) -\
            set( self.get_languages_with_word_separator() )
        )

    #
    # If separator for either alphabet/syllable/word (we shall refer as token) is None, this means there is no
    # way to identify the token. If the separator is '', means we can identify it by character (e.g. Chinese character,
    # Thai alphabet, Korean alphabet inside a Korean character/syllable).
    #
    def get_split_token(
            self,
            lang,
            level
    ):
        self.__check_lang(lang = lang)
        lang_dict = self.langs[lang]

        have_alphabet = lang_dict[LangFeatures.C_HAVE_ALPHABET]
        have_syl_sep  = lang_dict[LangFeatures.C_HAVE_SYL_SEP]
        syl_sep_type  = lang_dict[LangFeatures.C_SYL_SEP_TYPE]
        have_word_sep = lang_dict[LangFeatures.C_HAVE_WORD_SEP]
        word_sep_type = lang_dict[LangFeatures.C_WORD_SEP_TYPE]

        if level == LangFeatures.LEVEL_ALPHABET:
            # If a language has alphabets, the separator is by character, otherwise return NA
            if have_alphabet:
                return ''
            else:
                return None
        elif level == LangFeatures.LEVEL_SYLLABLE:
            if have_syl_sep:
                if syl_sep_type == LangFeatures.T_CHAR:
                    return ''
                elif syl_sep_type == LangFeatures.T_SPACE:
                    return ' '
                else:
                    return None
        elif level == LangFeatures.LEVEL_UNIGRAM:
            # Return language specific word separator if exists.
            # Return language specific syllable separator if exists.
            if have_word_sep:
                if word_sep_type == LangFeatures.T_CHAR:
                    return ''
                elif word_sep_type == LangFeatures.T_SPACE:
                    return ' '
                else:
                    return None
            elif have_syl_sep:
                if syl_sep_type == LangFeatures.T_CHAR:
                    return ''
                elif syl_sep_type == LangFeatures.T_SPACE:
                    return ' '
                else:
                    return None

        return None

    def get_alphabet_type(self, lang):
        # Language index
        lang_index = self.langfeatures.index[self.langfeatures[LangFeatures.C_LANG_ID]==lang].tolist()
        if len(lang_index) == 0:
            return None
        lang_index = lang_index[0]

        return self.langfeatures[LangFeatures.C_CHAR_TYPE][lang_index]


if __name__ == '__main__':
    def demo_1():
        lf = LangFeatures()
        print ( lf.langfeatures )
        return

    def demo_2():
        lf = LangFeatures()

        for lang in lf.langfeatures[LangFeatures.C_LANG_ID]:
            print ( lang + ':alphabet=[' + str(lf.get_split_token(lang, LangFeatures.LEVEL_ALPHABET)) + ']' )
            print ( lang + ':syllable=[' + str(lf.get_split_token(lang, LangFeatures.LEVEL_SYLLABLE)) + ']' )
            print ( lang + ':unigram=[' + str(lf.get_split_token(lang, LangFeatures.LEVEL_UNIGRAM)) + ']' )
            print ( lang + ':Character Type = ' + lf.get_alphabet_type(lang) )
            print ( lang + ':Token same as charset = ' + str(lf.is_lang_token_same_with_charset(lang=lang)))

    def demo_3():
        lf = LangFeatures()
        print ( lf.langfeatures )

        print ( 'Languages with word separator: ' + str(lf.get_languages_with_word_separator()) )
        print ( 'Languages with syllable separator:' + str(lf.get_languages_with_syllable_separator()) )
        print ( 'Languages with only syllable separator:' + str(lf.get_languages_with_only_syllable_separator()))

    demo_1()
    demo_2()
    demo_3()
