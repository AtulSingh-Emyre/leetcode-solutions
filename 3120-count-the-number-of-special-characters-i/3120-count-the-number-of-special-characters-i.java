class Solution {
    public int numberOfSpecialChars(String word) {
        boolean[] lower = new boolean[26];
        boolean[] upper = new boolean[26];
        int res = 0;
        for(char c: word.toCharArray()) {
            if(c<='Z') upper[c-'A'] = true;
            else lower[c-'a'] = true;
        }
        for (int i=0;i<26;i++) {
            if(lower[i] && upper[i]) res++;
        }
        return res;
    }
}