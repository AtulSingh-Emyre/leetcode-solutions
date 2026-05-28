public class TrieNode {
    int index;
    int len;
    TrieNode[] children;

    public TrieNode() {
        this.index = Integer.MAX_VALUE;
        this.len = Integer.MAX_VALUE;
        this.children = new TrieNode[26];
    }

    public void updateParam(int ind, int l) {
        if( (l < this.len) || (l == this.len && ind<this.index) ) {
            this.len = l;
            this.index = ind;
        }
    }

    public void insertChar(char c, int ind, int l) {
        if(this.children[c-'a'] == null) {
                this.children[c-'a'] = new TrieNode();
                
        }
        this.children[c-'a'].updateParam(ind,l);
    }

    public int getIndexOfNode() {
        return this.index;
    }

    public TrieNode getNode(char c) {
        return this.children[c-'a'];
    }
}

class Solution {

    public int[] stringIndices(String[] wordsContainer, String[] wordsQuery) {
        TrieNode root = new TrieNode();
        for (int w = 0; w < wordsContainer.length;w++) {
            char[] cc = wordsContainer[w].toCharArray();
            root.updateParam(w,cc.length);
            TrieNode iter = root;
            for(int i = cc.length-1; i>=0;i--) {
                char c = cc[i];
                iter.insertChar(c,w,cc.length);
                iter = iter.getNode(c);
            }
        }
        int[] result = new int[wordsQuery.length];
        for(int w = 0; w< wordsQuery.length;w++) {
            char[] cc = wordsQuery[w].toCharArray();
            TrieNode iter = root;
            for(int i = cc.length-1; i>=0 ; i--) {
                if(iter.getNode(cc[i]) == null) {
                    break;
                } else iter = iter.getNode(cc[i]);
            }
            result[w] = iter.getIndexOfNode();
        }
        return result;
        
    }
}