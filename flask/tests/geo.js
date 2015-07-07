/**
 * Query the airfields table for airfields near the given position.
 * @param dbCon DB connection
 * @param ref_lat latitude
 * @param ref_lon longitude
 * @return Answer the airfield nearest to the given position as array
 *          of objects: id, designator, latitude, longitude.
 *          Answer <code>null</code> if their is no airfield near the
 *          given position plus or minus 0.1 degrees.
 */
private Object[] rangeQuery(final SQLiteDatabase dbCon, final double ref_lat, final double ref_lon) {
    if( DEBUG )
        Log.d( TAG, "rangeQuery lat=" + ref_lat + ", lon=" + ref_lon);
    final SQLiteQueryBuilder qb = new SQLiteQueryBuilder();
    qb.setTables(AirfieldsTable.TABLE_NAME);
    final String[] whereArgs = new String[] {
            Double.toString(ref_lat - 0.1d), Double.toString(ref_lat + 0.1d),
            Double.toString(ref_lon - 0.1d), Double.toString(ref_lon + 0.1d)
    };
    final Cursor crsr = qb.query(dbCon, allFields(), AirfieldsTable.RANGE_CLAUSE, whereArgs, null, null, null);
    final Object[] val = this.scanForNearest(crsr, ref_lat, ref_lon);
    crsr.close();
    if( DEBUG )
        Log.d( TAG, "scanForNearest returned " + val);
    return val;
}