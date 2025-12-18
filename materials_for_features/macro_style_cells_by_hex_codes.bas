REM  *****  BASIC  *****
Rem
Rem ColorStyles - multicolored cell (create styles)
Rem (©) Vladislav Orlov aka JohnSUN, Kyiv, 2018
Rem This program is free software: you can redistribute it and/or modify
Rem it under the terms of the GNU General Public License as published by
Rem the Free Software Foundation, either version 3 of the License, or
Rem (at your option) any later version.
Rem
Rem This program is distributed in the hope that it will be useful,
Rem but WITHOUT ANY WARRANTY; without even the implied warranty of
Rem MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
Rem GNU General Public License for more details.
Rem
Rem You should have received a copy of the GNU General Public License
Rem along with this program.  If not, see <http://www.gnu.org/licenses/>.
Rem
Rem mailto:johnsun@i.ua

Option Explicit

Function crtStylesIfNeed(sColorCode As String, Optional newStylePrefix As String) As String
Dim oStyleFamilies As Variant, oCellStyles As Variant, oENames As Variant
Dim oBaseCellStyle As Variant, nameParentStyle As String
Dim oNewCellStyle As Variant, nameNewStyle As String, nCellBackColor As Long
	If IsMissing(newStylePrefix) Then newStylePrefix = "c_"
	nameNewStyle = newStylePrefix & sColorCode
	crtStylesIfNeed = nameNewStyle

	oStyleFamilies = ThisComponent.getStyleFamilies()
	oCellStyles = oStyleFamilies.getByName("CellStyles")
	
	If oCellStyles.hasByName(nameNewStyle) Then Exit Function ' Present, nothing to do

	If oCellStyles.hasByName(newStylePrefix) Then
		oBaseCellStyle = oCellStyles.getByName(newStylePrefix)
	Else
		oBaseCellStyle = oCellStyles.getByIndex(0) ' "Default"
	EndIf
	nameParentStyle = oBaseCellStyle.getName()
	
	oNewCellStyle = ThisComponent.createInstance("com.sun.star.style.CellStyle")
	oNewCellStyle.ParentStyle = nameParentStyle
	oCellStyles.insertByName(nameNewStyle, oNewCellStyle)
	nCellBackColor = CLng(Replace(sColorCode,"#","&H"))
	oNewCellStyle.setPropertyValue("CellBackColor", nCellBackColor)
	oNewCellStyle.setPropertyValue("NumberFormat", oBaseCellStyle.NumberFormat)
End Function

