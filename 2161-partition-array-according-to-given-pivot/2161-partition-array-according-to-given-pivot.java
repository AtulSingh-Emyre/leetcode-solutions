class Solution {
    public int[] pivotArray(int[] nums, int pivot) {
        ArrayList<Integer> pl = new ArrayList<>();
        ArrayList<Integer> pp = new ArrayList<>();
        ArrayList<Integer> pr = new ArrayList<>();
        for(int n: nums) {
            if(n<pivot) pl.add(n);
            if(n == pivot) pp.add(n);
            if(n>pivot) pr.add(n);
        }
        int[] res = new int[nums.length];
        for(int i=0;i<pl.size();i++) res[i] = pl.get(i);
        for(int i=0;i<pp.size();i++) res[i+pl.size()] = pp.get(i);
        for(int i=0;i<pr.size();i++) res[i+pl.size()+pp.size()] = pr.get(i);
        return res;
    }
}