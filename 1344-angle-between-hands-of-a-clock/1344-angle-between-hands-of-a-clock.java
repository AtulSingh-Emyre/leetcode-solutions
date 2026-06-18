class Solution {
    public double angleClock(int hour, int minutes) {
        double h_angle = (hour%12)*30 + (minutes)/2.0;
        double m_angle = minutes*6;
        double res = Math.max(h_angle,m_angle) - Math.min(m_angle,h_angle);
        res = Math.min(res, 360-res);
        return res;

    }
}