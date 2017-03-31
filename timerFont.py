# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 22:30:04 2017

@author: johns
"""

from fontTools import ttLib as TTLib
import re 
import subprocess 
import math 

class TimerFont: 
    
    _H_ADV = 0
    
    def __init__(self, font_name, font_file_path, p_size): 
        self.name = font_name
        self.font = TTLib.TTFont(font_file_path) 
        
        self.pt_size = p_size
        
        self.ascent = self.font["hhea"].ascent 
        self.descent = self.font["hhea"].descent 
        self.lineGap = self.font["hhea"].lineGap 
        self.unitsPerEm = self.font["head"].unitsPerEm 
        
        self.scale = self.pt_size / self.unitsPerEm 
        self.ascent = (int(math.ceil(self.scale * self.ascent)))
        self.descent = (int(math.ceil(self.scale * self.descent))) 
        self.lineGap = (int(math.ceil(self.scale * self.lineGap))) 
        
        
        self.adv_col = self._findColonAdvance(self.font) 
        self.adv_col = (int(math.ceil(self.adv_col * self.scale))) 
        
        self.baseline = self.ascent + self.lineGap 
        
        glyf_list = self._findTabSub(self.font) 
        if(glyf_list is not None): 
            self.tnum = True 
            print("tabular")
        else: 
            self.tnum = False 
            glyf_list = self._findGlyfNotTab(self.font) 
        
        self.adv_dig = self._findMaxAdvance(glyf_list, self.font) 
        self.adv_dig = (int(math.ceil(self.scale * self.adv_dig)))
        del glyf_list 
        
        
        
    
    
    def _findFontFile(self, font_name): 
        shell_call_args = ["magick", "-list", "font"] 
        shell_call = subprocess.Popen(shell_call_args, stdout = subprocess.PIPE) 
        font_list = shell_call.communicate()[0].decode(encoding = 'ascii')
            
        fname_exp = re.compile(r"^\s*Font: " + font_name + r".?$", re.M)
        fpath_exp = re.compile(r"^\s*glyphs: ([^\r]*)\r$", re.M)
        
        fname_match = fname_exp.search(font_list) 
        if(fname_match is None): 
            print("Can't find font file.") 
        fpath_match = fpath_exp.search(font_list, fname_match.start()) 
    
        if fpath_match is None: 
            return None
        
        return fpath_match.group(1) 
        
    def _findColonAdvance(self, font): 
        col_adv = 0
        uni_colon = (ord(":"))
        for t in font["cmap"].tables: 
            if(t.isUnicode()): 
                if(uni_colon in t.cmap): 
                    col_glyf = t.cmap[uni_colon] 
                    col_glyf_adv = font["hmtx"].metrics[col_glyf][self._H_ADV] 
                    if(col_glyf_adv > col_adv): 
                        col_adv = col_glyf_adv
        return col_adv
        
        
    def _findTabSub(self, font): 
        # init set to return
        glyf_set = set()
        if("GSUB" not in font): 
            return None 
        latn_script = None 
        for record in font["GSUB"].table.ScriptList.ScriptRecord: 
            if(record.ScriptTag == "latn"): 
                latn_script = record.Script 
        latn_feat_idx = latn_script.DefaultLangSys.FeatureIndex 
        tnum_feat = None
        for feat_idx in latn_feat_idx: 
            feat_rec = font["GSUB"].table.FeatureList.FeatureRecord[feat_idx] 
            if(feat_rec.FeatureTag == "tnum"): 
                tnum_feat = feat_rec.Feature 
        if(tnum_feat is None): 
            return None 
        for idx in tnum_feat.LookupListIndex: 
            sub_table_list = font["GSUB"].table.LookupList.Lookup[idx].SubTable
            for subtable in sub_table_list: 
                mapping = subtable.ExtSubTable.mapping 
                for i in mapping: 
                    glyf_set.add(mapping[i])
        if(len(glyf_set) < 1): 
            return None 
        return list(glyf_set)

    def _findGlyfNotTab(self, font): 
        glyf_set = set() 
        unitablelist = [t for t in font["cmap"].tables if t.isUnicode()] 
        for t in unitablelist: 
            code_pts = t.cmap.keys() 
            for i in range(10): 
                if ord(str(i)) in code_pts: 
                    glyf_set.add(t.cmap[ord(str(i))]) 
        return list(glyf_set)  

    def _findMaxAdvance(self, glyf_list, font): 
        adv_max = 0 
        for glyf in glyf_list: 
            advance = font["hmtx"].metrics[glyf][self._H_ADV] 
            if(advance > adv_max): 
                adv_max = advance 
        return adv_max
        
