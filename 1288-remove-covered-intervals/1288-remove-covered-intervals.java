class Solution {
    public int removeCoveredIntervals(int[][] intervals) {
        Arrays.sort(intervals, (int[] a,int[] b) -> (a[0] != b[0]? Integer.compare(a[0],b[0]): Integer.compare(b[1],a[1])));
        int c = 0;
        int d = 0;
        int cnt = 0;
        for(int[] interval: intervals) {
            int a = interval[0];
            int b = interval[1];
            if(c<=a && b<=d) continue;
            cnt++;
            c = a;
            d = b;
        }
        return cnt;
    }
}